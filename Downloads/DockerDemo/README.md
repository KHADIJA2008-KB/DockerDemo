# Docker Demo Application

A simple full-stack application demonstrating Docker and Docker Compose usage.

## Architecture

- **Frontend**: HTML/CSS/JavaScript served with Nginx
- **Backend**: Python Flask REST API
- **Orchestration**: Docker Compose

## Features

- ✅ Simple message board application
- ✅ RESTful API with Flask
- ✅ Modern responsive UI
- ✅ Docker containers for both services
- ✅ Docker Compose orchestration
- ✅ Health checks and auto-restart

## Project Structure

```
DockerDemo/
├── backend/
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Backend Docker configuration
├── frontend/
│   ├── index.html         # Main HTML file
│   ├── styles.css         # Styles
│   ├── app.js             # JavaScript logic
│   ├── nginx.conf         # Nginx configuration
│   └── Dockerfile         # Frontend Docker configuration
├── docker-compose.yml     # Docker Compose configuration
└── README.md             # This file
```

## Prerequisites

- Docker installed
- Docker Compose installed

## Running the Application

1. **Start the application:**
   ```bash
   docker-compose up -d
   ```

2. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

3. **Stop the application:**
   ```bash
   docker-compose down
   ```

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /api/messages` - Get all messages
- `POST /api/message` - Add a new message

## Docker Commands

```bash
# Build and start containers
docker-compose up --build

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down

# Remove containers and volumes
docker-compose down -v

# Rebuild containers
docker-compose up --build --force-recreate
```

## Development

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Frontend Development
Open `index.html` directly in a browser or use a local server.

## Troubleshooting

- If ports are already in use, modify them in `docker-compose.yml`
- Check logs: `docker-compose logs`
- Restart containers: `docker-compose restart`
- Rebuild images: `docker-compose build --no-cache`

