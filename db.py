import sqlite3
from models import ChatTurn, ChatTurnResponse
from typing import List
from datetime import datetime


DB_PATH = "data/chat_history.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS chat_turns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT NOT NULL,
            response TEXT NOT NULL,
            tokens_used INTEGER NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def insert_chat_turn(prompt: str, response: str, tokens_used: int) -> int:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    timestamp = datetime.utcnow().isoformat()
    c.execute('''
        INSERT INTO chat_turns (prompt, response, tokens_used, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (prompt, response, tokens_used, timestamp))
    turn_id = c.lastrowid
    conn.commit()
    conn.close()
    return turn_id


def get_last_20_turns() -> List['ChatTurnResponse']:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT id, prompt, response, tokens_used, timestamp
        FROM chat_turns
        ORDER BY id DESC
        LIMIT 20
    ''')
    rows = c.fetchall()
    conn.close()
    from models import ChatTurnResponse
    # Return all fields for each row
    return [ChatTurnResponse(
        id=row[0],
        prompt=row[1],
        response=row[2],
        tokens_used=row[3],
        timestamp=row[4]
    ) for row in rows]
