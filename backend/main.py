import os
import asyncio
import tempfile
import time
import httpx
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.security import APIKeyHeader
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from rag import add_document, build_rag_prompt, retrieve, get_stats

# ── CONFIG ────────────────────────────────────────
API_KEY     = os.getenv("API_KEY",     "mypassword123")
OLLAMA_URL  = os.getenv("OLLAMA_URL",  "http://localhost:11434")
PIPER_VOICE = os.getenv("PIPER_VOICE", "./voices/en_US-lessac-medium.onnx")

# ── APP ───────────────────────────────────────────
app = FastAPI(title="RAG AI", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = APIKeyHeader(name="X-API-Key")

def verify(key: str = Depends(security)):
    if key != API_KEY:
        raise HTTPException(401, detail="Wrong API Key")
    return key

# ── MODELS ────────────────────────────────────────
class ChatReq(BaseModel):
    message   : str
    model     : str  = "phi3:mini"
    use_rag   : bool = True

class TTSReq(BaseModel):
    text: str

# ── OLLAMA HELPER ─────────────────────────────────
async def ask_ollama(model: str, prompt: str) -> str:
    async with httpx.AsyncClient(timeout=180) as c:
        try:
            r = await c.post(f"{OLLAMA_URL}/api/generate",
                json={"model": model, "prompt": prompt, "stream": False})
            r.raise_for_status()
            return r.json()["response"]
        except Exception as e:
            raise HTTPException(503, detail=f"Ollama error: {e}")

# ── HEALTH — no auth ──────────────────────────────
@app.get("/health")
async def health():
    result = {"api": "ok", "ollama": "error", "models": [], "db": get_stats()}
    try:
        async with httpx.AsyncClient(timeout=5) as c:
            r = await c.get(f"{OLLAMA_URL}/api/tags")
            result["ollama"] = "ok"
            result["models"] = [m["name"] for m in r.json().get("models", [])]
    except:
        pass
    return result

# ── CHAT + RAG ────────────────────────────────────
@app.post("/chat")
async def chat(req: ChatReq, _=Depends(verify)):
    start    = time.time()
    chunks   = retrieve(req.message) if req.use_rag else []
    prompt   = build_rag_prompt(req.message, chunks)
    reply    = await ask_ollama(req.model, prompt)
    return {
        "reply"         : reply,
        "model"         : req.model,
        "rag_used"      : len(chunks) > 0,
        "chunks_found"  : len(chunks),
        "time_sec"      : round(time.time() - start, 2)
    }

# ── UPLOAD DOC ────────────────────────────────────
@app.post("/upload")
async def upload(file: UploadFile = File(...), _=Depends(verify)):
    content = await file.read()
    if file.filename.endswith(".txt"):
        text = content.decode("utf-8", errors="ignore")
    elif file.filename.endswith(".pdf"):
        try:
            import pdfplumber, io
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                text = "\n".join(p.extract_text() or "" for p in pdf.pages)
        except Exception as e:
            raise HTTPException(400, f"PDF error: {e}")
    else:
        raise HTTPException(400, "Only .txt and .pdf supported")

    result = add_document(text, file.filename.replace(" ", "_"), {"file": file.filename})
    return {"ok": True, "file": file.filename, **result}

# ── TTS ───────────────────────────────────────────
@app.post("/tts")
async def tts(req: TTSReq, _=Depends(verify)):
    tmp = tempfile.mktemp(suffix=".wav", dir="/tmp")
    try:
        proc = await asyncio.create_subprocess_shell(
            f'echo "{req.text}" | piper --model {PIPER_VOICE} --output_file {tmp}',
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL
        )
        await proc.communicate()
        if not os.path.exists(tmp):
            raise HTTPException(500, "TTS failed")

        def stream():
            with open(tmp, "rb") as f:
                yield from f
            os.unlink(tmp)

        return StreamingResponse(stream(), media_type="audio/wav",
            headers={"Content-Disposition": "attachment; filename=reply.wav"})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

# ── DB STATS ──────────────────────────────────────
@app.get("/stats")
async def stats(_=Depends(verify)):
    return get_stats()

# ── SERVE FRONTEND — must be last ─────────────────
app.mount("/", StaticFiles(directory="../frontend", html=True), name="ui")