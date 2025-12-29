"""Chat system models for item recovery communication"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class ChatRoom(Base):
    __tablename__ = "chat_rooms"
    
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    finder_name = Column(String(100), nullable=False)
    finder_phone = Column(String(20), nullable=False)
    seeker_name = Column(String(100), nullable=False)
    seeker_phone = Column(String(20), nullable=False)
    status = Column(String(20), default="active")  # active, completed, cancelled
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    messages = relationship("ChatMessage", back_populates="room")
    item = relationship("Item", back_populates="chat_room")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("chat_rooms.id"), nullable=False)
    sender_type = Column(String(10), nullable=False)  # finder, seeker
    sender_name = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    message_type = Column(String(20), default="text")  # text, location, recovery_plan
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    room = relationship("ChatRoom", back_populates="messages")

class RecoveryPlan(Base):
    __tablename__ = "recovery_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("chat_rooms.id"), nullable=False)
    plan_type = Column(String(20), nullable=False)  # meetup, delivery, pickup
    location = Column(String(200))
    date_time = Column(DateTime)
    instructions = Column(Text)
    status = Column(String(20), default="proposed")  # proposed, accepted, completed
    created_by = Column(String(10), nullable=False)  # finder, seeker
    created_at = Column(DateTime(timezone=True), server_default=func.now())