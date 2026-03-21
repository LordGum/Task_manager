from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TodoBase(BaseModel):
    title: str
    description: str
    status: str = "в ожидании"
    priority: int = 0

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = None

class TodoResponse(TodoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True