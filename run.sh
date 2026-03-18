#!/bin/bash
echo "Starting RAG Application..."
echo "=========================="

# Start backend in background
cd backend
uvicorn main:app --host 0.0.0.0 --port 7860 --reload &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 3

# Start frontend
cd ../frontend
python -m http.server 8000

# When you press Ctrl+C, kill backend too
kill $BACKEND_PID