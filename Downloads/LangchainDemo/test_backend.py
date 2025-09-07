#!/usr/bin/env python3
"""
Simple test script to verify the backend is working
"""

import requests
import json
import time

def test_backend():
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Multi-Agent Brainstormer Backend")
    print("=" * 50)
    
    try:
        # Test root endpoint
        print("1. Testing root endpoint...")
        response = requests.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # Test agents endpoint
        print("\n2. Testing agents endpoint...")
        response = requests.get(f"{base_url}/agents")
        print(f"   Status: {response.status_code}")
        agents_data = response.json()
        print(f"   Found {len(agents_data['agents'])} agents:")
        for agent in agents_data['agents']:
            print(f"   - {agent['name']} ({agent['role']})")
        
        # Test session creation
        print("\n3. Testing session creation...")
        response = requests.post(f"{base_url}/sessions")
        print(f"   Status: {response.status_code}")
        session_data = response.json()
        print(f"   Session ID: {session_data['session_id']}")
        
        # Test chat with single agent
        print("\n4. Testing chat with single agent...")
        chat_data = {
            "message": "What do you think about AI in business?",
            "agent_name": "marketer"
        }
        response = requests.post(f"{base_url}/chat", json=chat_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            chat_response = response.json()
            print(f"   Agent: {chat_response['agent_name']}")
            print(f"   Response: {chat_response['response'][:100]}...")
        
        print("\n✅ Backend test completed successfully!")
        print("\n🌐 You can now:")
        print(f"   - Open {base_url}/docs to see the API documentation")
        print(f"   - Open frontend/index.html in your browser to use the UI")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend. Make sure it's running on port 8000")
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_backend()
