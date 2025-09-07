from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, List, Optional
import json
import asyncio
import uuid
from datetime import datetime

# Import our existing agent system
from main import MultiAgentBrainstormer, SpecialistAgent

app = FastAPI(title="Multi-Agent Brainstormer API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global brainstormer instance
brainstormer = MultiAgentBrainstormer()

# Store active sessions
active_sessions: Dict[str, dict] = {}

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.session_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        
        if session_id not in self.session_connections:
            self.session_connections[session_id] = []
        self.session_connections[session_id].append(websocket)

    def disconnect(self, websocket: WebSocket, session_id: str):
        self.active_connections.remove(websocket)
        if session_id in self.session_connections:
            self.session_connections[session_id].remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_to_session(self, message: str, session_id: str):
        if session_id in self.session_connections:
            for connection in self.session_connections[session_id]:
                await connection.send_text(message)

manager = ConnectionManager()

# Pydantic models for API requests/responses
class ChatMessage(BaseModel):
    message: str
    agent_name: Optional[str] = None
    session_id: Optional[str] = None

class BrainstormRequest(BaseModel):
    idea: str
    rounds: int = 3
    session_id: Optional[str] = None

class AgentResponse(BaseModel):
    agent_name: str
    role: str
    response: str
    timestamp: datetime

class SessionInfo(BaseModel):
    session_id: str
    created_at: datetime
    agents: List[Dict[str, str]]

# API Endpoints

@app.get("/")
async def root():
    return {"message": "Multi-Agent Brainstormer API", "version": "1.0.0"}

@app.get("/agents")
async def get_agents():
    """Get list of available agents"""
    agents_info = []
    for key, agent in brainstormer.agents.items():
        agents_info.append({
            "id": key,
            "name": agent.name,
            "role": agent.role,
            "persona": agent.persona,
            "expertise": agent.expertise
        })
    return {"agents": agents_info}

@app.post("/sessions")
async def create_session():
    """Create a new brainstorming session"""
    session_id = str(uuid.uuid4())
    active_sessions[session_id] = {
        "id": session_id,
        "created_at": datetime.now(),
        "messages": [],
        "brainstorm_results": None
    }
    
    return {
        "session_id": session_id,
        "message": "Session created successfully"
    }

@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """Get session information"""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return active_sessions[session_id]

@app.post("/chat")
async def chat_with_agent(request: ChatMessage):
    """Send a message to a specific agent or all agents"""
    try:
        if request.agent_name:
            # Determine if it's a predefined agent or a custom expert
            if request.agent_name.startswith("custom_"):
                # For custom experts, persona and expertise should be sent from frontend
                # For now, we'll assume the frontend sends enough info to recreate it if needed.
                # A more robust solution might involve storing custom experts in a database.
                # For this iteration, if not found, we raise an error.
                # In future, if the custom agent details are sent with the chat message,
                # we could dynamically create it here.
                raise HTTPException(status_code=400, detail="Custom agent not supported via direct /chat endpoint yet without full details.")
            
            if request.agent_name not in brainstormer.agents:
                raise HTTPException(status_code=400, detail="Agent not found")
            
            agent = brainstormer.agents[request.agent_name]
            response = agent.respond(request.message)
            
            return {
                "agent_name": agent.name,
                "role": agent.role,
                "response": response,
                "timestamp": datetime.now()
            }
        else:
            # Chat with all agents
            responses = []
            for key, agent in brainstormer.agents.items():
                response = agent.respond(request.message)
                responses.append({
                    "agent_name": agent.name,
                    "role": agent.role,
                    "response": response,
                    "timestamp": datetime.now()
                })
            
            return {"responses": responses}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/brainstorm")
async def start_brainstorm(request: BrainstormRequest):
    """Start a brainstorming session"""
    try:
        # Create session if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        if session_id not in active_sessions:
            active_sessions[session_id] = {
                "id": session_id,
                "created_at": datetime.now(),
                "messages": [],
                "brainstorm_results": None
            }
        
        # Run brainstorming session
        results = brainstormer.brainstorm_idea(request.idea, request.rounds)
        
        # Store results
        active_sessions[session_id]["brainstorm_results"] = results
        
        return {
            "session_id": session_id,
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket endpoint for real-time chat
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect(websocket, session_id)
    
    # Create session if it doesn't exist
    if session_id not in active_sessions:
        active_sessions[session_id] = {
            "id": session_id,
            "created_at": datetime.now(),
            "messages": [],
            "brainstorm_results": None
        }
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data["type"] == "chat":
                # Handle chat message
                user_message = message_data["message"]
                agent_id = message_data.get("agent_id") # Use agent_id here
                expert_details = message_data.get("expert_details") # Added for custom experts
                
                # Store user message
                active_sessions[session_id]["messages"].append({
                    "type": "user",
                    "message": user_message,
                    "timestamp": datetime.now().isoformat()
                })
                
                if agent_id:
                    agent = None
                    if agent_id.startswith("custom_") and expert_details:
                        # Create a temporary SpecialistAgent for custom expert
                        agent = SpecialistAgent(
                            name=expert_details["name"],
                            role=expert_details["role"],
                            persona=expert_details["persona"],
                            expertise=expert_details["expertise"],
                            session_id=session_id # Associate with current session
                        )
                    elif agent_id in brainstormer.agents:
                        agent = brainstormer.agents[agent_id]
                        agent.session_id = session_id # Ensure existing agent uses current session_id
                    
                    if agent is None:
                        await manager.send_personal_message(
                            json.dumps({"type": "error", "message": "Agent not found or custom expert details missing."}),
                            websocket
                        )
                        return

                    # Single agent response
                    response = agent.respond(user_message)
                    
                    response_data = {
                        "type": "agent_response",
                        "agent_name": agent.name,
                        "role": agent.role,
                        "response": response,
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    # Store response
                    active_sessions[session_id]["messages"].append(response_data)
                    
                    # Send to client
                    await manager.send_personal_message(json.dumps(response_data), websocket)
                    
                else:
                    # This case should ideally not happen with the new frontend logic
                    # where an expert is always selected. However, we'll keep a fallback.
                    # All agents respond
                    for key, agent in brainstormer.agents.items():
                        # Ensure existing agent uses current session_id
                        agent.session_id = session_id
                        response = agent.respond(user_message)
                        
                        response_data = {
                            "type": "agent_response",
                            "agent_name": agent.name,
                            "role": agent.role,
                            "response": response,
                            "timestamp": datetime.now().isoformat()
                        }
                        
                        # Store response
                        active_sessions[session_id]["messages"].append(response_data)
                        
                        # Send to client
                        await manager.send_personal_message(json.dumps(response_data), websocket)
                        
                        # Small delay between agents
                        await asyncio.sleep(1)
            
            elif message_data["type"] == "brainstorm":
                # Handle brainstorming request
                idea = message_data["idea"]
                rounds = message_data.get("rounds", 3)
                
                # Send status update
                await manager.send_personal_message(
                    json.dumps({
                        "type": "brainstorm_started",
                        "idea": idea,
                        "rounds": rounds
                    }), 
                    websocket
                )
                
                # Run brainstorming (this could be made async for better UX)
                results = brainstormer.brainstorm_idea(idea, rounds)
                
                # Store results
                active_sessions[session_id]["brainstorm_results"] = results
                
                # Send results
                await manager.send_personal_message(
                    json.dumps({
                        "type": "brainstorm_complete",
                        "results": results
                    }), 
                    websocket
                )
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)
    except Exception as e:
        await manager.send_personal_message(
            json.dumps({
                "type": "error",
                "message": str(e)
            }), 
            websocket
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend:app", host="0.0.0.0", port=8000, reload=True)
