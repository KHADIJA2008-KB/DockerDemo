#!/bin/bash

# Multi-Agent Brainstormer Startup Script

echo "🚀 Starting Multi-Agent Brainstormer"
echo "=================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. You'll be prompted for your Google API key."
fi

# Start backend server
echo "🔧 Starting backend server..."
uvicorn backend:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Test backend
echo "🧪 Testing backend..."
python test_backend.py

# Check if backend is running
if ! curl -s http://localhost:8000/ > /dev/null; then
    echo "❌ Backend failed to start"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo ""
echo "✅ Application started successfully!"
echo ""
echo "🌐 Access your application:"
echo "   - Backend API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - Frontend: Open frontend/index.html in your browser"
echo ""
echo "📋 Available endpoints:"
echo "   - GET  /agents - List all agents"
echo "   - POST /sessions - Create new session"
echo "   - POST /chat - Chat with agents"
echo "   - POST /brainstorm - Start brainstorm session"
echo "   - WS   /ws/{session_id} - WebSocket connection"
echo ""
echo "🛑 To stop the application, press Ctrl+C"

# Keep script running and handle cleanup
trap "echo '🛑 Stopping application...'; kill $BACKEND_PID 2>/dev/null; exit 0" INT

# Wait for user to stop
wait $BACKEND_PID
