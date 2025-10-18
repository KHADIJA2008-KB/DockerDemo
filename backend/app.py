from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# In-memory storage for demo
messages = []

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the Backend API!",
        "status": "running",
        "endpoints": {
            "/api/messages": "GET - Get all messages",
            "/api/message": "POST - Add a new message"
        }
    })

@app.route('/api/messages', methods=['GET'])
def get_messages():
    return jsonify({
        "success": True,
        "messages": messages,
        "count": len(messages)
    })

@app.route('/api/message', methods=['POST'])
def add_message():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({
            "success": False,
            "error": "Message text is required"
        }), 400
    
    message = {
        "id": len(messages) + 1,
        "text": data['text'],
        "timestamp": data.get('timestamp', '')
    }
    messages.append(message)
    
    return jsonify({
        "success": True,
        "message": message
    }), 201

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

