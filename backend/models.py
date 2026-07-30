from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    display_name = Column(String, nullable=False)
    points = Column(JSON, nullable=False)          # which 3 landmark indices define this exercise
    down_threshold = Column(Float, nullable=False)
    up_threshold = Column(Float, nullable=False)


class WorkoutSession(Base):
    __tablename__ = "workout_sessions"

    id = Column(Integer, primary_key=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())

    reps = relationship("RepLog", back_populates="session")


class RepLog(Base):
    __tablename__ = "rep_logs"

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("workout_sessions.id"), nullable=False)
    rep_number = Column(Integer, nullable=False)
    min_angle = Column(Float, nullable=True)
    max_angle = Column(Float, nullable=True)

    session = relationship("WorkoutSession", back_populates="reps")