from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base
from datetime import datetime

class Transaction(Base):
    __tablename__ = "transactions"

    id=Column(Integer, primary_key=True, index=True)
    user_id= Column(Integer, index=True)
    vendor=Column(String, index=True)
    subject= Column(String)
    amount=Column(Float)
    category=Column(String, nullable=True)
    email_id=Column(String, unique=True, index=True)
    date=Column(DateTime, default=datetime.utcnow)
    created_at=Column(DateTime, default=datetime.utcnow)
    updated_at=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

