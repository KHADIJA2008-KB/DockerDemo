# Docker Demo Application

A simple full-stack application demonstrating Docker and Docker Compose usage.
 
 
Screenshots:
 
1.   <img width="1610" height="944" alt="image" src="https://github.com/user-attachments/assets/845d1577-2fe6-4705-b458-9b973c8b46f5" />

-----

2.   <img width="926" height="970" alt="image" src="https://github.com/user-attachments/assets/5c69c938-d8ae-4ea0-b9e7-e6a50fb04499" />

-----

3.   <img width="1063" height="553" alt="image" src="https://github.com/user-attachments/assets/8b616986-edba-4d48-aa4e-1bc7067b760f" />


-----


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
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:5001

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

## Pushing to GitHub

1. **Create a new repository on GitHub** (e.g., `DockerDemo`)

2. **Update the remote URL:**
   ```bash
   git remote set-url origin https://github.com/YOUR_USERNAME/DockerDemo.git
   ```

3. **Push the code:**
   ```bash
   git push -u origin main
   ```

## Troubleshooting

- If ports are already in use, modify them in `docker-compose.yml`
- Check logs: `docker-compose logs`
- Restart containers: `docker-compose restart`
- Rebuild images: `docker-compose build --no-cache`

