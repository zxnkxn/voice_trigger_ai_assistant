from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from db.database import Base


class DialogMessage(Base):
    __tablename__ = "dialog_messages"

    id = Column(Integer, primary_key=True)
    toy_id = Column(String, index=True, nullable=False)
    role = Column(String, nullable=False)  # "user" | "assistant"
    text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
