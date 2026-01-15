from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base


class PracticeSession(Base):
    __tablename__ = "practice_sessions"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Metadata
    s3_key = Column(String, unique=True, index=True, nullable=False)
    duration_seconds = Column(Float, nullable=False)
    note_count = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())