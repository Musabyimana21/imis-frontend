"""Chat API endpoints for item recovery communication"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import datetime
from ..core.database import get_db
from ..models.enhanced_models import AnonymousItem, AnonymousPayment, ChatMessage
from pydantic import BaseModel

router = APIRouter()

class ChatMessageCreate(BaseModel):
    room_id: str
    sender_phone: str
    message: str

class ChatMessageResponse(BaseModel):
    id: int
    sender_phone: str
    message: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class RecoveryPlanCreate(BaseModel):
    room_id: str
    plan_type: str  # meetup, delivery, pickup
    location: str = None
    date_time: str = None
    instructions: str = None
    created_by_phone: str

@router.post("/chat/send", response_model=Dict)
async def send_message(message_data: ChatMessageCreate, db: Session = Depends(get_db)):
    """Send a chat message"""
    try:
        # Create new message
        message = ChatMessage(
            room_id=message_data.room_id,
            sender_phone=message_data.sender_phone,
            message=message_data.message
        )
        
        db.add(message)
        db.commit()
        db.refresh(message)
        
        return {
            "success": True,
            "message_id": message.id,
            "message": "Message sent successfully"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")

@router.get("/chat/{room_id}/messages", response_model=List[ChatMessageResponse])
async def get_messages(room_id: str, db: Session = Depends(get_db)):
    """Get all messages for a chat room"""
    try:
        messages = db.query(ChatMessage).filter(
            ChatMessage.room_id == room_id
        ).order_by(ChatMessage.created_at.asc()).all()
        
        return messages
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get messages: {str(e)}")

@router.post("/chat/recovery-plan", response_model=Dict)
async def create_recovery_plan(plan_data: RecoveryPlanCreate, db: Session = Depends(get_db)):
    """Create a recovery plan"""
    try:
        # Create system message for recovery plan
        plan_message = f"📋 Recovery Plan Proposed:\n"
        plan_message += f"Type: {plan_data.plan_type.title()}\n"
        
        if plan_data.location:
            plan_message += f"Location: {plan_data.location}\n"
        if plan_data.date_time:
            plan_message += f"Date/Time: {plan_data.date_time}\n"
        if plan_data.instructions:
            plan_message += f"Instructions: {plan_data.instructions}\n"
            
        plan_message += f"\nReply 'ACCEPT' to confirm or suggest changes."
        
        message = ChatMessage(
            room_id=plan_data.room_id,
            sender_phone=plan_data.created_by_phone,
            message=plan_message
        )
        
        db.add(message)
        db.commit()
        
        return {
            "success": True,
            "message": "Recovery plan created successfully"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create recovery plan: {str(e)}")

@router.get("/chat/room/{item_id}/info", response_model=Dict)
async def get_chat_room_info(item_id: int, db: Session = Depends(get_db)):
    """Get chat room information for an item"""
    try:
        # Get item details
        item = db.query(AnonymousItem).filter(AnonymousItem.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        # Check if payment was made (contact unlocked)
        payment = db.query(AnonymousPayment).filter(
            AnonymousPayment.item_id == item_id,
            AnonymousPayment.status == "completed"
        ).first()
        
        if not payment:
            raise HTTPException(status_code=403, detail="Payment required to access chat")
        
        room_id = f"item_{item_id}"
        
        return {
            "room_id": room_id,
            "item_title": item.title,
            "item_status": item.status,
            "finder_name": item.reporter_name,
            "finder_phone": item.reporter_phone,
            "seeker_phone": payment.payer_phone,
            "location": item.location_name,
            "recovery_options": [
                {
                    "type": "meetup",
                    "title": "Meet in Person",
                    "description": "Arrange to meet at a safe public location",
                    "icon": "🤝"
                },
                {
                    "type": "delivery",
                    "title": "Home Delivery",
                    "description": "Finder delivers item to your location",
                    "icon": "🚚"
                },
                {
                    "type": "pickup",
                    "title": "Pickup Location",
                    "description": "Pick up item from finder's preferred location",
                    "icon": "📍"
                }
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get chat room info: {str(e)}")