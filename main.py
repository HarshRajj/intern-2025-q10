
#!/usr/bin/env python3
"""
Q10 FastAPI Microservice with Database Logging
Copyright (c) 2025 HarshRajj
Licensed under the MIT License
"""

import os
import shutil
from datetime import datetime
from fastapi import FastAPI, HTTPException, Response
from db import init_db, insert_chat_turn, get_last_20_turns
from models import ChatTurn, ChatTurnResponse
from typing import List
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from chatbot.prompt_utils import get_prompt_template
from chatbot.rate_limiter import TokenBucket
from chatbot.cache_utils import get_cached_response


import shutil
app = FastAPI()

# Global chatbot objects
llm = None
memory = None
prompt = None
chain = None
bucket = None

def initialize_chatbot():
    """Initialize chatbot components"""
    global llm, memory, prompt, chain, bucket
    init_db()
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        # In testing mode, we can initialize without the API key
        # The /chat endpoint will handle the missing key gracefully
        llm = None
        memory = ConversationBufferMemory(k=4, return_messages=True)
        prompt = get_prompt_template()
        chain = None
        bucket = TokenBucket(rate=10, per=60)
        print("Warning: GOOGLE_API_KEY not found. Chat functionality will be limited.")
    else:
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)
        memory = ConversationBufferMemory(k=4, return_messages=True)
        prompt = get_prompt_template()
        chain = ConversationChain(llm=llm, memory=memory, prompt=prompt)
        bucket = TokenBucket(rate=10, per=60)

@app.on_event("startup")
def startup():
    initialize_chatbot()

# Initialize immediately for testing environments
if bucket is None:
    initialize_chatbot()


# Accepts: {"prompt": "..."}

@app.post("/chat", response_model=ChatTurnResponse)
def log_chat_turn(turn: ChatTurn):
    global chain, bucket
    try:
        if not bucket.consume():
            raise HTTPException(status_code=429, detail="Rate limit exceeded. Please wait.")
        # Generate bot response using Q7 logic
        try:
            response, cached, elapsed = get_cached_response(turn.prompt, chain)
        except Exception as llm_error:
            # Handle API quota or other LLM errors gracefully
            response = f"Error: LLM service unavailable ({str(llm_error)[:100]})"
        # Estimate tokens used (simple whitespace split, or use a tokenizer if available)
        tokens_used = len(turn.prompt.split()) + len(str(response).split())
        turn_id = insert_chat_turn(turn.prompt, response, tokens_used)
        # Fetch the inserted row to get the timestamp
        last_turns = get_last_20_turns()
        inserted = next((row for row in last_turns if row.id == turn_id), None)
        if inserted is None:
            raise HTTPException(status_code=500, detail="Inserted chat turn not found.")
        return inserted
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history", response_model=List[ChatTurnResponse])
def get_history():
    return get_last_20_turns()

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Q10 FastAPI Microservice",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


    from models import ChatTurn, ChatTurnResponse
    from typing import List
    from dotenv import load_dotenv
    from langchain.memory import ConversationBufferMemory
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain.chains import ConversationChain
    from chatbot.prompt_utils import get_prompt_template
    from chatbot.rate_limiter import TokenBucket
    from chatbot.cache_utils import get_cached_response

# Endpoint to export chat history as a human-readable CSV file
import csv
from fastapi.responses import StreamingResponse
from io import StringIO

@app.get("/export_history_csv")
def export_history_csv():
    rows = get_last_20_turns()[::-1]  # oldest first
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "prompt", "response", "tokens_used", "timestamp"])
    for row in rows:
        writer.writerow([row.id, row.prompt, row.response, row.tokens_used, row.timestamp])
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=chat_history.csv"})

@app.get("/export_history_txt")
def export_history_txt():
    rows = get_last_20_turns()[::-1]  # oldest first
    output = StringIO()
    output.write("Chat History Export\n")
    output.write("==================\n\n")
    for row in rows:
        output.write(f"ID: {row.id}\n")
        output.write(f"Timestamp: {row.timestamp}\n")
        output.write(f"Prompt: {row.prompt}\n")
        output.write(f"Response: {row.response}\n")
        output.write(f"Tokens Used: {row.tokens_used}\n")
        output.write("-" * 50 + "\n\n")
    
    # Save to data folder
    import os
    os.makedirs("data", exist_ok=True)
    with open("data/chat_history_export.txt", "w", encoding="utf-8") as f:
        f.write(output.getvalue())
    
    output.seek(0)
    return StreamingResponse(output, media_type="text/plain", headers={"Content-Disposition": "attachment; filename=chat_history.txt"})
