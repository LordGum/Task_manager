from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String, default="в ожидании")
    priority = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)