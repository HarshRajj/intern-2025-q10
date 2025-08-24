# Q9: Database Logging - Chat Turn Logging API

FastAPI application that logs every chat turn to SQLite database with comprehensive chat history management and export capabilities.

## Features

- **Database Logging**: Persists chat turns with id, prompt, response, tokens_used, timestamp
- **AI Integration**: Uses Google Gemini with rate limiting, caching, and memory
- **Export Options**: CSV and human-readable text exports
- **Interactive API**: Swagger UI documentation at `/docs`

## Endpoints

- `POST /chat`: Send a prompt and get AI response (logged to database)
  - Request: `{ "prompt": "Your question here" }`
  - Response: Full chat turn with id, prompt, response, tokens_used, timestamp
- `GET /history`: Get the last 20 chat turns (most recent first)
- `GET /export_history_csv`: Download chat history as CSV file
- `GET /export_history_txt`: Download/save chat history as readable text

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/intern-2025-q9.git
   cd intern-2025-q9
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment:**
   Create a `.env` file with your Google API key:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

4. **Run the API:**
   ```bash
   python -m uvicorn main:app --reload
   ```

5. **Access the API:**
   - Interactive docs: http://127.0.0.1:8000/docs
   - API base: http://127.0.0.1:8000

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
