from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from app.core.config import settings
import logging

# Create SQLAlchemy engine
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Integer, default=1)

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    symbol = Column(String, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    direction = Column(String)  # "Up", "Down", "Neutral"
    confidence = Column(Float)
    actual = Column(String, nullable=True)  # Can be updated later

def init_db():
    """Initialize the database by creating all tables."""
    try:
        Base.metadata.create_all(bind=engine)
        logging.info("Database tables created successfully")
    except Exception as e:
        logging.error(f"Error creating database tables: {e}")
        raise

def get_db():
    """Get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def log_prediction(db: Session, user_id: int, symbol: str, direction: str, confidence: float):
    """Log a prediction to the database."""
    prediction = Prediction(
        user_id=user_id,
        symbol=symbol,
        direction=direction,
        confidence=confidence
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction

def get_prediction_history(db: Session, user_id: int):
    """Get prediction history for a user."""
    return db.query(Prediction).filter(Prediction.user_id == user_id).order_by(Prediction.date.desc()).all() 