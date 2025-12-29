from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class ItemStatus(str, Enum):
    LOST = "lost"
    FOUND = "found"
    MATCHED = "matched"
    RECOVERED = "recovered"

class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class ItemCategory(str, Enum):
    PHONE = "phone"
    WALLET = "wallet"
    KEYS = "keys"
    BAG = "bag"
    DOCUMENTS = "documents"
    ELECTRONICS = "electronics"
    JEWELRY = "jewelry"
    OTHER = "other"

# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone: Optional[str] = None
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    phone: Optional[str]
    role: str
    is_active: bool
    avatar_url: Optional[str]
    bio: Optional[str]
    location: Optional[str]
    items_lost: int
    items_found: int
    items_recovered: int
    reputation_score: float
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserPublicProfile(BaseModel):
    id: int
    full_name: str
    avatar_url: Optional[str]
    bio: Optional[str]
    location: Optional[str]
    items_found: int
    items_recovered: int
    reputation_score: float
    
    class Config:
        from_attributes = True

# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    user_id: Optional[int] = None

# Item Schemas
class ItemCreate(BaseModel):
    title: str
    description: str
    category: ItemCategory
    status: ItemStatus
    location_name: str
    latitude: float
    longitude: float
    date_lost_found: datetime
    brand: Optional[str] = None
    model: Optional[str] = None
    color: Optional[str] = None
    size: Optional[str] = None
    distinctive_features: Optional[str] = None
    reward_amount: Optional[float] = 0.0
    contact_method: Optional[str] = "both"
    allow_public_contact: Optional[bool] = False
    
    @validator('latitude')
    def validate_latitude(cls, v):
        if not -90 <= v <= 90:
            raise ValueError('Latitude must be between -90 and 90')
        return v
    
    @validator('longitude')
    def validate_longitude(cls, v):
        if not -180 <= v <= 180:
            raise ValueError('Longitude must be between -180 and 180')
        return v

class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[ItemCategory] = None
    status: Optional[ItemStatus] = None
    location_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    color: Optional[str] = None
    size: Optional[str] = None
    distinctive_features: Optional[str] = None
    reward_amount: Optional[float] = None
    is_urgent: Optional[bool] = None

class ItemResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    status: str
    location_name: str
    latitude: float
    longitude: float
    brand: Optional[str]
    model: Optional[str]
    color: Optional[str]
    size: Optional[str]
    distinctive_features: Optional[str]
    primary_image_url: str
    image_urls: List[str]
    date_lost_found: datetime
    created_at: datetime
    is_active: bool
    is_featured: bool
    is_urgent: bool
    reward_amount: float
    reward_currency: str
    contact_method: str
    allow_public_contact: bool
    view_count: int
    match_count: int
    message_count: int
    user: UserPublicProfile
    
    class Config:
        from_attributes = True

class ItemSummary(BaseModel):
    id: int
    title: str
    category: str
    status: str
    location_name: str
    primary_image_url: str
    reward_amount: float
    created_at: datetime
    distance_km: Optional[float] = None
    
    class Config:
        from_attributes = True

# Match Schemas
class MatchResponse(BaseModel):
    id: int
    item_id: int
    matched_item_id: int
    similarity_score: float
    text_similarity: float
    location_similarity: float
    distance_km: float
    category_match: bool
    brand_match: bool
    color_match: bool
    confidence_level: str
    match_reason: Optional[str]
    created_at: datetime
    matched_item: ItemResponse
    
    class Config:
        from_attributes = True

class MatchSummary(BaseModel):
    id: int
    similarity_score: float
    distance_km: float
    confidence_level: str
    matched_item: ItemSummary
    
    class Config:
        from_attributes = True

# Message Schemas
class MessageCreate(BaseModel):
    receiver_id: int
    item_id: int
    content: str
    message_type: Optional[str] = "text"

class MessageResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    item_id: int
    content: str
    message_type: str
    is_read: bool
    created_at: datetime
    sender: UserPublicProfile
    receiver: UserPublicProfile
    
    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    item_id: int
    other_user: UserPublicProfile
    last_message: MessageResponse
    unread_count: int
    
    class Config:
        from_attributes = True

# Payment Schemas
class PaymentCreate(BaseModel):
    item_id: int
    amount: float
    payment_method: str  # mtn_momo, airtel_money, bank
    phone_number: Optional[str] = None
    description: Optional[str] = None

class PaymentResponse(BaseModel):
    id: int
    user_id: int
    item_id: int
    amount: float
    currency: str
    payment_method: str
    phone_number: Optional[str]
    status: str
    transaction_id: Optional[str]
    external_reference: Optional[str]
    description: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class PaymentInitiate(BaseModel):
    payment_id: int
    payment_url: Optional[str]
    qr_code: Optional[str]
    instructions: str

# Commission Schemas
class CommissionCreate(BaseModel):
    item_id: int
    amount: float
    rate: Optional[float] = 0.10

class CommissionResponse(BaseModel):
    id: int
    item_id: int
    payment_id: Optional[int]
    amount: float
    rate: float
    currency: str
    status: str
    created_at: datetime
    paid_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Review Schemas
class ReviewCreate(BaseModel):
    reviewed_id: int
    item_id: Optional[int] = None
    rating: int
    comment: Optional[str] = None
    
    @validator('rating')
    def validate_rating(cls, v):
        if not 1 <= v <= 5:
            raise ValueError('Rating must be between 1 and 5')
        return v

class ReviewResponse(BaseModel):
    id: int
    reviewer_id: int
    reviewed_id: int
    item_id: Optional[int]
    rating: int
    comment: Optional[str]
    created_at: datetime
    reviewer: UserPublicProfile
    
    class Config:
        from_attributes = True

# Notification Schemas
class NotificationResponse(BaseModel):
    id: int
    title: str
    message: str
    type: str
    item_id: Optional[int]
    related_user_id: Optional[int]
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Admin Schemas
class AdminStats(BaseModel):
    total_users: int
    total_items: int
    total_lost_items: int
    total_found_items: int
    total_recovered_items: int
    total_matches: int
    total_messages: int
    total_payments: float
    total_commissions: float
    active_users_today: int
    new_items_today: int
    successful_recoveries_today: int

class AdminUserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    phone: Optional[str]
    role: str
    is_active: bool
    is_verified: bool
    items_lost: int
    items_found: int
    items_recovered: int
    reputation_score: float
    last_login: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Search and Filter Schemas
class ItemSearchFilters(BaseModel):
    category: Optional[ItemCategory] = None
    status: Optional[ItemStatus] = None
    location: Optional[str] = None
    radius_km: Optional[float] = 50
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    has_reward: Optional[bool] = None
    min_reward: Optional[float] = None
    max_reward: Optional[float] = None

class SearchResponse(BaseModel):
    items: List[ItemResponse]
    total: int
    page: int
    per_page: int
    has_next: bool
    has_prev: bool

# Anonymous (No Login) Schemas
class AnonymousItemCreate(BaseModel):
    title: str
    description: str
    category: ItemCategory
    status: ItemStatus
    location_name: str
    latitude: float
    longitude: float
    date_lost_found: datetime
    contact_name: str
    contact_phone: str
    contact_email: Optional[EmailStr] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    color: Optional[str] = None
    reward_amount: Optional[float] = 0.0

class AnonymousItemResponse(BaseModel):
    id: int
    tracking_code: str
    title: str
    description: str
    category: str
    status: str
    location_name: str
    primary_image_url: str
    reward_amount: float
    created_at: datetime
    contact_instructions: str
    
    class Config:
        from_attributes = True

# System Schemas
class HealthCheck(BaseModel):
    status: str
    database: str
    version: str
    timestamp: datetime

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    errors: Optional[List[str]] = None