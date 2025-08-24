from pydantic import BaseModel
from typing import Optional


class ChatTurn(BaseModel):
    prompt: str

class ChatTurnResponse(BaseModel):
    id: int
    prompt: str
    response: str
    tokens_used: int
    timestamp: str
