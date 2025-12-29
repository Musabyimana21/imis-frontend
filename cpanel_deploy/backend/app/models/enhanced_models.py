from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Enum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..core.database import Base

try:
    from geoalchemy2 import Geography
    HAS_POSTGIS = True
except ImportError:
    HAS_POSTGIS = False

class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"

class ItemStatus(str, enum.Enum):
    LOST = "lost"
    FOUND = "found"
    MATCHED = "matched"
    RECOVERED = "recovered"

class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class ItemCategory(str, enum.Enum):
    PHONE = "phone"
    WALLET = "wallet"
    KEYS = "keys"
    BAG = "bag"
    DOCUMENTS = "documents"
    ELECTRONICS = "electronics"
    JEWELRY = "jewelry"
    OTHER = "other"

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20))
    role = Column(Enum(UserRole), default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_code = Column(String(10))
    reset_token = Column(String(255))
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Profile info
    avatar_url = Column(String(500))
    bio = Column(Text)
    location = Column(String(255))
    
    # Statistics
    items_lost = Column(Integer, default=0)
    items_found = Column(Integer, default=0)
    items_recovered = Column(Integer, default=0)
    reputation_score = Column(Float, default=5.0)
    
    # Relationships
    items = relationship("Item", back_populates="user")
    messages_sent = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    messages_received = relationship("Message", foreign_keys="Message.receiver_id", back_populates="receiver")
    payments = relationship("Payment", back_populates="user")
    reviews = relationship("Review", foreign_keys="Review.reviewer_id", back_populates="reviewer")
    received_reviews = relationship("Review", foreign_keys="Review.reviewed_id", back_populates="reviewed")

class Item(Base):
    __tablename__ = "items"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Basic info
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(Enum(ItemCategory), nullable=False)
    status = Column(Enum(ItemStatus), nullable=False)
    
    # Location info
    location_name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    # Use simple string for location to avoid PostGIS dependency
    location = Column(String(500))
    
    # Additional details
    brand = Column(String(100))
    model = Column(String(100))
    color = Column(String(50))
    size = Column(String(50))
    distinctive_features = Column(Text)
    
    # Images
    image_urls = Column(JSON, default=list)
    primary_image_url = Column(String(500), default="/api/placeholder/400/300")
    
    # Dates
    date_lost_found = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Status flags
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    is_urgent = Column(Boolean, default=False)
    
    # Reward info
    reward_amount = Column(Float, default=0.0)
    reward_currency = Column(String(10), default="RWF")
    
    # Contact preferences
    contact_method = Column(String(20), default="both")  # phone, email, both
    allow_public_contact = Column(Boolean, default=False)
    
    # AI matching metadata
    text_vector = Column(Text)  # For search optimization
    match_keywords = Column(JSON, default=list)
    
    # Statistics
    view_count = Column(Integer, default=0)
    match_count = Column(Integer, default=0)
    message_count = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="items")
    matches = relationship("Match", foreign_keys="Match.item_id", back_populates="item")
    messages = relationship("Message", back_populates="item")
    payments = relationship("Payment", back_populates="item")

class Match(Base):
    __tablename__ = "matches"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    matched_item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    
    # Scoring
    similarity_score = Column(Float, nullable=False)
    text_similarity = Column(Float, nullable=False)
    location_similarity = Column(Float, nullable=False)
    category_match = Column(Boolean, default=False)
    brand_match = Column(Boolean, default=False)
    color_match = Column(Boolean, default=False)
    
    # Distance
    distance_km = Column(Float, nullable=False)
    
    # Status
    is_confirmed = Column(Boolean, default=False)
    is_dismissed = Column(Boolean, default=False)
    confidence_level = Column(String(20), default="medium")  # low, medium, high
    
    # Metadata
    match_reason = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    item = relationship("Item", foreign_keys=[item_id], back_populates="matches")
    matched_item = relationship("Item", foreign_keys=[matched_item_id])

class Message(Base):
    __tablename__ = "messages"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    
    # Content
    content = Column(Text, nullable=False)
    message_type = Column(String(20), default="text")  # text, image, location, system
    
    # Status
    is_read = Column(Boolean, default=False)
    is_deleted_by_sender = Column(Boolean, default=False)
    is_deleted_by_receiver = Column(Boolean, default=False)
    
    # Metadata
    read_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    sender = relationship("User", foreign_keys=[sender_id], back_populates="messages_sent")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="messages_received")
    item = relationship("Item", back_populates="messages")

class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    
    # Payment details
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="RWF")
    payment_method = Column(String(50), nullable=False)  # mtn_momo, airtel_money, bank
    phone_number = Column(String(20))
    
    # Status
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    
    # External references
    transaction_id = Column(String(100), unique=True)
    external_reference = Column(String(100))
    
    # Metadata
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="payments")
    item = relationship("Item", back_populates="payments")

class Commission(Base):
    __tablename__ = "commissions"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    payment_id = Column(Integer, ForeignKey("payments.id"))
    
    # Commission details
    amount = Column(Float, nullable=False)
    rate = Column(Float, default=0.10)  # 10%
    currency = Column(String(10), default="RWF")
    
    # Status
    status = Column(String(20), default="pending")  # pending, paid, cancelled
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime)

class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reviewed_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"))
    
    # Review content
    rating = Column(Integer, nullable=False)  # 1-5 stars
    comment = Column(Text)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    reviewer = relationship("User", foreign_keys=[reviewer_id], back_populates="reviews")
    reviewed = relationship("User", foreign_keys=[reviewed_id], back_populates="received_reviews")

class Notification(Base):
    __tablename__ = "notifications"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Content
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String(50), nullable=False)  # match, message, payment, system
    
    # References
    item_id = Column(Integer, ForeignKey("items.id"))
    related_user_id = Column(Integer, ForeignKey("users.id"))
    
    # Status
    is_read = Column(Boolean, default=False)
    is_sent = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    read_at = Column(DateTime)

class SystemSettings(Base):
    __tablename__ = "system_settings"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AnonymousItem(Base):
    __tablename__ = "anonymous_items"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Reporter info
    reporter_name = Column(String(255), nullable=False)
    reporter_phone = Column(String(20), nullable=False)
    
    # Item details
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False)
    
    # Location
    location_name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Image
    image_url = Column(Text)
    
    # Tracking
    tracking_code = Column(String(50), unique=True, nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AnonymousPayment(Base):
    __tablename__ = "anonymous_payments"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("anonymous_items.id"), nullable=False)
    
    # Payment details
    payer_phone = Column(String(20), nullable=False)
    payment_method = Column(String(50), nullable=False)
    transaction_id = Column(String(100), unique=True, nullable=False)
    status = Column(String(20), default="pending")
    amount = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Room/Item reference
    room_id = Column(String(100), nullable=False)
    
    # Message details
    sender_phone = Column(String(20), nullable=False)
    message = Column(Text, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(100), nullable=False)
    resource_type = Column(String(100), nullable=False)
    resource_id = Column(Integer)
    details = Column(JSON)
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)