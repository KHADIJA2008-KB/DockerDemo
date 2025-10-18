// Backend API URL - will be proxied through nginx
const API_URL = 'http://localhost:5001';

// Check backend health on page load
window.addEventListener('DOMContentLoaded', () => {
    checkBackendHealth();
    loadMessages();
    
    // Allow Enter key to submit message
    document.getElementById('messageInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addMessage();
        }
    });
});

async function checkBackendHealth() {
    const statusIndicator = document.getElementById('statusIndicator');
    statusIndicator.className = 'status-checking';
    statusIndicator.textContent = 'Checking...';
    
    try {
        const response = await fetch(`${API_URL}/health`);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            statusIndicator.className = 'status-healthy';
            statusIndicator.textContent = '✓ Connected';
        } else {
            throw new Error('Unhealthy');
        }
    } catch (error) {
        statusIndicator.className = 'status-error';
        statusIndicator.textContent = '✗ Disconnected';
        console.error('Backend health check failed:', error);
    }
}

async function loadMessages() {
    try {
        const response = await fetch(`${API_URL}/api/messages`);
        const data = await response.json();
        
        if (data.success) {
            displayMessages(data.messages);
            document.getElementById('messageCount').textContent = data.count;
        }
    } catch (error) {
        console.error('Error loading messages:', error);
        showError('Failed to load messages');
    }
}

function displayMessages(messages) {
    const messageList = document.getElementById('messageList');
    
    if (messages.length === 0) {
        messageList.innerHTML = '<p class="empty-state">No messages yet. Add one above!</p>';
        return;
    }
    
    messageList.innerHTML = messages.map(msg => `
        <div class="message-item">
            <div class="message-text">${escapeHtml(msg.text)}</div>
            <div class="message-time">${msg.timestamp || 'Just now'}</div>
        </div>
    `).join('');
}

async function addMessage() {
    const input = document.getElementById('messageInput');
    const text = input.value.trim();
    
    if (!text) {
        alert('Please enter a message');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/api/message`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                timestamp: new Date().toLocaleString()
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            input.value = '';
            loadMessages();
            checkBackendHealth();
        } else {
            showError(data.error || 'Failed to add message');
        }
    } catch (error) {
        console.error('Error adding message:', error);
        showError('Failed to add message. Is the backend running?');
    }
}

function showError(message) {
    alert(message);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

