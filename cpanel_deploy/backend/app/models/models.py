from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..core.database import Base

class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"

class ItemStatus(str, enum.Enum):
    LOST = "lost"
    FOUND = "found"
    MATCHED = "matched"
    RECOVERED = "recovered"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    phone = Column(String(20))
    role = Column(Enum(UserRole), default=UserRole.USER)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    items = relationship("Item", back_populates="user")
    messages_sent = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    messages_received = relationship("Message", foreign_keys="Message.receiver_id", back_populates="receiver")

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    status = Column(Enum(ItemStatus), nullable=False)
    location_name = Column(String(255))
    location = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    image_url = Column(String(500), default="{{item_image_placeholder}}")
    date_lost_found = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    user = relationship("User", back_populates="items")
    matches = relationship("Match", foreign_keys="Match.item_id", back_populates="item")

class Match(Base):
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    matched_item_id = Column(Integer, ForeignKey("items.id"))
    similarity_score = Column(Float)
    distance_km = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    item = relationship("Item", foreign_keys=[item_id], back_populates="matches")
    matched_item = relationship("Item", foreign_keys=[matched_item_id])

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    content = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    sender = relationship("User", foreign_keys=[sender_id], back_populates="messages_sent")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="messages_received")

class Commission(Base):
    __tablename__ = "commissions"
    
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    rate = Column(Float, default=0.10)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
