# 🦙 Local LLM Voice & Text Chatbot — Llama Powered

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Llama](https://img.shields.io/badge/Model-Llama_Local-orange?style=flat-square)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red?style=flat-square&logo=streamlit)
![Offline](https://img.shields.io/badge/Runs-100%25_Offline-brightgreen?style=flat-square)
![Status](https://img.shields.io/badge/Stage-Complete-green?style=flat-square)

---

👤 **Author:** [Ashutosh](https://github.com/Ashutosh-AIBOT) · [LinkedIn](https://www.linkedin.com/in/ashutosh1975271/)
💼 **Portfolio:** [ashutosh-portfolio-kappa.vercel.app](https://ashutosh-portfolio-kappa.vercel.app/)

---

## 🧠 What This Does

A fully offline voice + text chatbot powered by a locally
running Llama model. No API keys. No internet required.
No data sent to any server. Everything runs on your machine.

1. **Problem** — Cloud LLM APIs cost money, send your
   data to external servers, and require internet
2. **Solution** — Run Llama locally via Ollama. Full
   voice + text chat with zero API costs and complete
   privacy. Works offline.

---

## ✨ Features

| Feature | Detail |
|---------|--------|
| 🎙️ Voice Input | Speak to the chatbot — Whisper transcribes locally |
| 💬 Text Input | Standard text conversation interface |
| 🦙 Local Llama | Llama model runs entirely on your machine |
| 🔒 100% Private | Zero data sent to external servers |
| 💰 Zero API Cost | No OpenAI, no Anthropic, no bills |
| 🔌 Offline Ready | Works without internet connection |

---

## 🏗️ Architecture
```
User Input
  ├── Voice → Whisper (local) → text
  └── Text  → direct input
        ↓
       UI
        ↓
Ollama Local Server
  → Llama model loaded in memory
  → Runs on CPU or GPU
  → Returns response locally
        ↓
Response displayed in Streamlit
  → Conversation history maintained
  → Optional TTS output
```

---

## ⚡ Quick Start
```bash
# 1. Install Ollama
# https://ollama.ai → Download and install

# 2. Pull Llama model
ollama pull llama2

# 3. Clone and run
git clone https://github.com/Ashutosh-AIBOT/local-llm-voice-text-chatbot.git
cd local-llm-voice-text-chatbot
pip install -r requirements.txt
streamlit run app.py
```

---

## 🛠️ Tech Stack

`Python` `Ollama` `Llama 2/3` `Whisper (local)` `Streamlit` `SoundDevice` `Git`

---

## 🌐 Links

| Resource | URL |
|----------|-----|
| 🐙 GitHub | [github.com/Ashutosh-AIBOT](https://github.com/Ashutosh-AIBOT) |
| 💼 Portfolio | [ashutosh-portfolio-kappa.vercel.app](https://ashutosh-portfolio-kappa.vercel.app/) |

---

## 👤 Author
**Ashutosh** · B.Tech Electronics Engineering · Batch 2026
```
