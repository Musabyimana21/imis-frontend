from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class ItemCreate(BaseModel):
    title: str
    description: str
    category: str
    status: str
    location_name: str
    latitude: float
    longitude: float
    date_lost_found: Optional[datetime] = None

class ItemResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    status: str
    location_name: str
    latitude: float
    longitude: float
    image_url: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class MatchResponse(BaseModel):
    id: int
    item_id: int
    matched_item_id: int
    similarity_score: float
    distance_km: float
    matched_item: ItemResponse
    
    class Config:
        from_attributes = True

class MessageCreate(BaseModel):
    receiver_id: int
    item_id: int
    content: str

class MessageResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    content: str
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class CommissionResponse(BaseModel):
    id: int
    item_id: int
    amount: float
    rate: float
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True
