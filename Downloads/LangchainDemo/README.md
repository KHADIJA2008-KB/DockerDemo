# 🧠 Multi-Agent Brainstormer

A dynamic AI-powered brainstorming system featuring multiple specialist agents that collaborate to analyze ideas, provide expert perspectives, and generate comprehensive plans.

## 🌟 Features

- **4 Specialist AI Agents**: Designer, Marketer, Engineer, and Investor
- **Real-time Chat Interface**: Chat with individual agents or the entire panel
- **Multi-round Brainstorming**: Structured brainstorming sessions with synthesis
- **WebSocket Support**: Real-time communication with instant responses
- **Modern Web UI**: Beautiful, responsive interface with Tailwind CSS
- **RESTful API**: Complete backend API for integration

## 🤖 Meet the Expert Panel

### Alex Chen - UX/UI Designer
- **Expertise**: User experience design, interface design, accessibility
- **Focus**: User-centered solutions, design systems, prototyping

### Sarah Martinez - Marketing Strategist  
- **Expertise**: Market research, brand positioning, digital marketing
- **Focus**: Customer acquisition, growth strategies, competitive analysis

### David Kim - Software Engineer
- **Expertise**: Software architecture, full-stack development, cloud infrastructure
- **Focus**: Technical feasibility, scalability, security

### Rachel Goldman - Venture Capitalist
- **Expertise**: Business model evaluation, financial projections, investment strategy
- **Focus**: Market size, ROI analysis, exit planning

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google Gemini API key

### Installation

1. **Clone and setup**:
   ```bash
   cd /home/khadijab/Downloads/LangchainDemo
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Set up environment**:
   ```bash
   # Create .env file (optional)
   echo "GOOGLE_API_KEY=your_api_key_here" > .env
   ```

3. **Start the application**:
   ```bash
   ./start_app.sh
   ```

   Or manually:
   ```bash
   # Start backend
   python backend.py
   
   # Open frontend/index.html in your browser
   ```

## 📖 Usage

### Web Interface
1. Open `frontend/index.html` in your browser
2. Select an agent or choose "All Agents"
3. Type your question or idea
4. Get instant responses from AI experts

### Brainstorming Sessions
1. Click "Start Brainstorm Session"
2. Enter your idea
3. Choose number of discussion rounds (2-5)
4. Watch agents debate and refine the concept
5. Receive a comprehensive final plan

### API Usage

**Chat with specific agent:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "How can I improve user engagement?", "agent_name": "designer"}'
```

**Start brainstorming:**
```bash
curl -X POST "http://localhost:8000/brainstorm" \
  -H "Content-Type: application/json" \
  -d '{"idea": "AI-powered fitness app", "rounds": 3}'
```

## 🏗️ Architecture

### Backend (`backend.py`)
- **FastAPI** web framework
- **WebSocket** support for real-time chat
- **RESTful API** endpoints
- **Session management** for multiple users
- **Agent orchestration** system

### Frontend (`frontend/index.html`)
- **Modern HTML5/CSS3/JavaScript**
- **Tailwind CSS** for styling
- **WebSocket client** for real-time updates
- **Responsive design** for mobile/desktop

### Core System (`main.py`)
- **SpecialistAgent** class with memory
- **MultiAgentBrainstormer** orchestrator
- **LangChain integration** with Google Gemini
- **Conversation management** and synthesis

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API status |
| GET | `/agents` | List all agents |
| POST | `/sessions` | Create new session |
| GET | `/sessions/{id}` | Get session info |
| POST | `/chat` | Send message to agent(s) |
| POST | `/brainstorm` | Start brainstorm session |
| WS | `/ws/{session_id}` | WebSocket connection |

## 🎨 Customization

### Adding New Agents
Edit `main.py` and add to `_create_agents()`:
```python
agents['new_agent'] = SpecialistAgent(
    name="Agent Name",
    role="Agent Role",
    persona="Agent personality...",
    expertise="Agent skills..."
)
```

### Modifying UI
Edit `frontend/index.html` to customize:
- Colors and styling (Tailwind CSS classes)
- Layout and components
- JavaScript functionality

## 🐛 Troubleshooting

### Backend won't start
- Check Python version: `python --version`
- Verify dependencies: `pip list`
- Check port 8000: `lsof -i :8000`

### Frontend can't connect
- Ensure backend is running on port 8000
- Check browser console for errors
- Verify WebSocket connection

### API key issues
- Set `GOOGLE_API_KEY` environment variable
- Or create `.env` file with your key
- Restart the application after adding key

## 📝 Development

### Project Structure
```
LangchainDemo/
├── main.py              # Core agent system
├── backend.py           # FastAPI backend
├── frontend/
│   └── index.html       # Web interface
├── requirements.txt     # Python dependencies
├── start_app.sh         # Startup script
├── test_backend.py      # Backend tests
└── README.md           # This file
```

### Running Tests
```bash
python test_backend.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review the logs in terminal
3. Ensure all dependencies are installed
4. Verify your Google API key is valid

---

**Built with ❤️ using LangChain, FastAPI, and Google Gemini**
