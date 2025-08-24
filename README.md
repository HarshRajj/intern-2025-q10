# Q10: Micro-service + CI/CD - FastAPI Chat Microservice

Production-ready FastAPI microservice with CI/CD pipeline for chat turn logging and history management. Containerized with Docker and automated deployment via GitHub Actions.

## Features

- **Microservice Architecture**: FastAPI-based service with health checks
- **Database Logging**: Persists chat turns with id, prompt, response, tokens_used, timestamp
- **AI Integration**: Google Gemini with rate limiting, caching, and memory
- **Export Capabilities**: CSV and human-readable text exports
- **Containerization**: Docker support with health checks
- **CI/CD Pipeline**: GitHub Actions with testing and container registry deployment
- **Production Ready**: Proper logging, error handling, and monitoring

## API Endpoints

- `POST /chat`: Send a prompt and get AI response (logged to database)
- `GET /history`: Get the last 20 chat turns (most recent first)
- `GET /health`: Health check endpoint for monitoring
- `GET /export_history_csv`: Download chat history as CSV file
- `GET /export_history_txt`: Download/save chat history as readable text

## Quick Start

### Using Docker (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/intern-2025-q10.git
   cd intern-2025-q10
   ```

2. **Set up environment:**
   ```bash
   echo "GOOGLE_API_KEY=your_api_key_here" > .env
   ```

3. **Run with Docker Compose:**
   ```bash
   docker-compose up
   ```

4. **Access the service:**
   - API: http://localhost:8000
   - Health check: http://localhost:8000/health
   - Documentation: http://localhost:8000/docs

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the service:**
   ```bash
   python -m uvicorn main:app --reload
   ```

## Testing

Run the test suite:
```bash
pytest tests/ -v
```

## CI/CD Pipeline

The GitHub Actions workflow automatically:
- ✅ Runs pytest on every push/PR
- ✅ Builds Docker image
- ✅ Pushes to GitHub Container Registry (GHCR)
- ✅ Supports automatic deployment

## Docker Deployment

**Build and run locally:**
```bash
docker build -t q10-microservice .
docker run -p 8000:8000 -e GOOGLE_API_KEY=your_key q10-microservice
```

**Pull from registry:**
```bash
docker pull ghcr.io/yourusername/intern-2025-q10:latest
docker run -p 8000:8000 -e GOOGLE_API_KEY=your_key ghcr.io/yourusername/intern-2025-q10:latest
```

## Usage Examples

**Send a chat message:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is artificial intelligence?"}'
```

**Check service health:**
```bash
curl http://localhost:8000/health
```

**Get chat history:**
```bash
curl http://localhost:8000/history
```

## File Structure

- `main.py` - FastAPI application and endpoints
- `db.py` - SQLite database operations
- `models.py` - Pydantic data models
- `chatbot/` - Chatbot logic (rate limiting, caching, prompts)
- `tests/` - Test suite with pytest
- `Dockerfile` - Container definition
- `docker-compose.yml` - Multi-container orchestration
- `.github/workflows/` - CI/CD pipeline configuration
- `data/` - Database files and exports

## Assignment Compliance

This project fulfills Q10 requirements:
- ✅ FastAPI micro-service with /chat POST and /history GET endpoints
- ✅ Dockerfile for containerization
- ✅ GitHub Actions workflow with pytest, build, and GHCR push
- ✅ Health check endpoint /health
- ✅ Production-ready microservice architecture

## Usage Examples

**Send a chat message:**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/chat" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{ "prompt": "What is AI?" }'
```

**Get chat history:**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/history" -Method GET
```

**Export history:**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/export_history_csv" -Method GET -OutFile "chat_history.csv"
```

## File Structure

- `main.py` - FastAPI application and endpoints
- `db.py` - SQLite database operations
- `models.py` - Pydantic data models
- `chatbot/` - Reused chatbot logic from Q7 (rate limiting, caching, prompts)
- `data/` - Database files and exports
- `requirements.txt` - Python dependencies

## Assignment Compliance

This project fulfills Q9 requirements:
- ✅ Persists every chat turn into SQLite: id, prompt, response, tokens_used, timestamp
- ✅ FastAPI endpoint GET /history to list the last 20 rows
- ✅ Additional features: POST /chat, export capabilities, error handling

## File Structure
- `main.py`: FastAPI app and endpoints
- `db.py`: SQLite logic
- `models.py`: Pydantic models
- `requirements.txt`: Dependencies
- `README.md`: This file
