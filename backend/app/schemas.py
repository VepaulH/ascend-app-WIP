
from pydantic import BaseModel, Field
from datetime import datetime

class EntryIn(BaseModel):
    mood: str | None = None
    habit: str | None = None
    duration: int | None = Field(default=None, description="minutes")
    notes: str | None = None
    timestamp: datetime | None = None
    user_id: int | None = 1

class EntryOut(EntryIn):
    id: int

class ChatIn(BaseModel):
    text: str
