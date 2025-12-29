from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from typing import List, Optional
from datetime import datetime
from ..core.database import get_db
from ..models.enhanced_models import Message, User, Item, Notification
from ..models.enhanced_schemas import MessageCreate, MessageResponse, ConversationResponse
from .auth import get_current_user
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/messages", tags=["messages"])

@router.post("/", response_model=MessageResponse)
def send_message(
    message: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Send a message about an item"""
    try:
        # Validate receiver exists
        receiver = db.query(User).filter(User.id == message.receiver_id).first()
        if not receiver:
            raise HTTPException(status_code=404, detail="Receiver not found")
        
        # Validate item exists
        item = db.query(Item).filter(Item.id == message.item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        # Check if sender can message about this item
        # Users can message if they own the item or if it's a different status item
        if item.user_id != current_user.id and item.user_id != message.receiver_id:
            # Check if this is a cross-status conversation (lost <-> found)
            sender_items = db.query(Item).filter(
                Item.user_id == current_user.id,
                Item.is_active == True
            ).all()
            
            # Allow if sender has items of opposite status
            opposite_status = "found" if item.status == "lost" else "lost"
            has_opposite_items = any(i.status == opposite_status for i in sender_items)
            
            if not has_opposite_items:
                raise HTTPException(
                    status_code=403, 
                    detail="You can only message about items when you have relevant items to discuss"
                )
        
        # Create message
        db_message = Message(
            sender_id=current_user.id,
            receiver_id=message.receiver_id,
            item_id=message.item_id,
            content=message.content,
            message_type=message.message_type
        )
        
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        
        # Update item message count
        item.message_count += 1
        db.commit()
        
        # Create notification for receiver
        notification = Notification(
            user_id=message.receiver_id,
            title="💬 New Message",
            message=f"You have a new message from {current_user.full_name} about '{item.title}'",
            type="message",
            item_id=message.item_id,
            related_user_id=current_user.id
        )
        db.add(notification)
        db.commit()
        
        logger.info(f"Message sent from user {current_user.id} to user {message.receiver_id} about item {message.item_id}")
        
        return db_message
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to send message")

@router.get("/conversations", response_model=List[ConversationResponse])
def get_conversations(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's message conversations grouped by item and other user"""
    try:
        # Get latest message for each conversation
        subquery = db.query(
            Message.item_id,
            func.case(
                [(Message.sender_id == current_user.id, Message.receiver_id)],
                else_=Message.sender_id
            ).label('other_user_id'),
            func.max(Message.id).label('latest_message_id')
        ).filter(
            or_(
                Message.sender_id == current_user.id,
                Message.receiver_id == current_user.id
            )
        ).group_by(
            Message.item_id,
            'other_user_id'
        ).subquery()
        
        # Get full conversation details
        conversations = db.query(
            Message,
            subquery.c.other_user_id
        ).join(
            subquery,
            Message.id == subquery.c.latest_message_id
        ).order_by(desc(Message.created_at)).limit(limit).all()
        
        result = []
        for message, other_user_id in conversations:
            # Get other user info
            other_user = db.query(User).filter(User.id == other_user_id).first()
            
            # Count unread messages in this conversation
            unread_count = db.query(Message).filter(
                and_(
                    Message.item_id == message.item_id,
                    Message.sender_id == other_user_id,
                    Message.receiver_id == current_user.id,
                    Message.is_read == False
                )
            ).count()
            
            result.append(ConversationResponse(
                item_id=message.item_id,
                other_user=other_user,
                last_message=message,
                unread_count=unread_count
            ))
        
        return result
        
    except Exception as e:
        logger.error(f"Error getting conversations: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve conversations")

@router.get("/conversation/{item_id}/{other_user_id}", response_model=List[MessageResponse])
def get_conversation_messages(
    item_id: int,
    other_user_id: int,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get messages in a specific conversation"""
    try:
        # Validate item exists
        item = db.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        # Validate other user exists
        other_user = db.query(User).filter(User.id == other_user_id).first()
        if not other_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get messages between current user and other user about this item
        messages = db.query(Message).filter(
            and_(
                Message.item_id == item_id,
                or_(
                    and_(
                        Message.sender_id == current_user.id,
                        Message.receiver_id == other_user_id
                    ),
                    and_(
                        Message.sender_id == other_user_id,
                        Message.receiver_id == current_user.id
                    )
                )
            )
        ).order_by(desc(Message.created_at)).offset(offset).limit(limit).all()
        
        # Mark messages as read (messages sent to current user)
        unread_messages = db.query(Message).filter(
            and_(
                Message.item_id == item_id,
                Message.sender_id == other_user_id,
                Message.receiver_id == current_user.id,
                Message.is_read == False
            )
        ).all()
        
        for msg in unread_messages:
            msg.is_read = True
            msg.read_at = datetime.utcnow()
        
        if unread_messages:
            db.commit()
        
        # Return messages in chronological order (oldest first)
        return list(reversed(messages))
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting conversation messages: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve messages")

@router.get("/unread-count")
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get total unread message count for user"""
    try:
        unread_count = db.query(Message).filter(
            and_(
                Message.receiver_id == current_user.id,
                Message.is_read == False
            )
        ).count()
        
        return {"unread_count": unread_count}
        
    except Exception as e:
        logger.error(f"Error getting unread count: {e}")
        raise HTTPException(status_code=500, detail="Failed to get unread count")

@router.put("/{message_id}/read")
def mark_message_read(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark a specific message as read"""
    try:
        message = db.query(Message).filter(
            and_(
                Message.id == message_id,
                Message.receiver_id == current_user.id
            )
        ).first()
        
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        
        message.is_read = True
        message.read_at = datetime.utcnow()
        db.commit()
        
        return {"message": "Message marked as read"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error marking message as read: {e}")
        raise HTTPException(status_code=500, detail="Failed to mark message as read")

@router.put("/conversation/{item_id}/{other_user_id}/read-all")
def mark_conversation_read(
    item_id: int,
    other_user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark all messages in a conversation as read"""
    try:
        messages = db.query(Message).filter(
            and_(
                Message.item_id == item_id,
                Message.sender_id == other_user_id,
                Message.receiver_id == current_user.id,
                Message.is_read == False
            )
        ).all()
        
        for message in messages:
            message.is_read = True
            message.read_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "message": f"Marked {len(messages)} messages as read",
            "count": len(messages)
        }
        
    except Exception as e:
        logger.error(f"Error marking conversation as read: {e}")
        raise HTTPException(status_code=500, detail="Failed to mark conversation as read")

@router.delete("/{message_id}")
def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a message (soft delete)"""
    try:
        message = db.query(Message).filter(Message.id == message_id).first()
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        
        # Users can only delete their own messages or messages sent to them
        if message.sender_id == current_user.id:
            message.is_deleted_by_sender = True
        elif message.receiver_id == current_user.id:
            message.is_deleted_by_receiver = True
        else:
            raise HTTPException(status_code=403, detail="Not authorized to delete this message")
        
        db.commit()
        
        return {"message": "Message deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting message: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete message")

@router.get("/search")
def search_messages(
    query: str = Query(..., min_length=1),
    item_id: Optional[int] = None,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search messages by content"""
    try:
        # Base query for user's messages
        base_query = db.query(Message).filter(
            or_(
                Message.sender_id == current_user.id,
                Message.receiver_id == current_user.id
            )
        )
        
        # Add item filter if specified
        if item_id:
            base_query = base_query.filter(Message.item_id == item_id)
        
        # Add text search
        messages = base_query.filter(
            Message.content.ilike(f"%{query}%")
        ).order_by(desc(Message.created_at)).limit(limit).all()
        
        return {
            "query": query,
            "results": messages,
            "count": len(messages)
        }
        
    except Exception as e:
        logger.error(f"Error searching messages: {e}")
        raise HTTPException(status_code=500, detail="Failed to search messages")

@router.get("/stats")
def get_message_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's messaging statistics"""
    try:
        sent_count = db.query(Message).filter(Message.sender_id == current_user.id).count()
        received_count = db.query(Message).filter(Message.receiver_id == current_user.id).count()
        unread_count = db.query(Message).filter(
            and_(
                Message.receiver_id == current_user.id,
                Message.is_read == False
            )
        ).count()
        
        # Count unique conversations
        conversations_count = db.query(
            func.count(func.distinct(
                func.case(
                    [(Message.sender_id == current_user.id, Message.receiver_id)],
                    else_=Message.sender_id
                )
            ))
        ).filter(
            or_(
                Message.sender_id == current_user.id,
                Message.receiver_id == current_user.id
            )
        ).scalar()
        
        return {
            "messages_sent": sent_count,
            "messages_received": received_count,
            "unread_messages": unread_count,
            "total_conversations": conversations_count,
            "response_rate": (sent_count / received_count * 100) if received_count > 0 else 0
        }
        
    except Exception as e:
        logger.error(f"Error getting message stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve message statistics")

@router.post("/quick-responses")
def get_quick_responses():
    """Get suggested quick responses for common scenarios"""
    return {
        "lost_item_responses": [
            "Hi! I think I found your item. Can you describe it in more detail?",
            "Hello! I have something that matches your description. When did you lose it?",
            "Hi there! I found an item that might be yours. Where exactly did you lose it?",
            "I believe I have your item. Can we arrange a meeting to verify?"
        ],
        "found_item_responses": [
            "Thank you for finding my item! Can we meet to verify it's mine?",
            "This looks like my item! When and where did you find it?",
            "I think this is mine! Can you tell me more details about where you found it?",
            "Yes, this is definitely mine! How can we arrange the return?"
        ],
        "verification_questions": [
            "Can you describe any distinctive features or markings?",
            "What color is it exactly?",
            "Are there any scratches or damage?",
            "Can you tell me the brand or model?",
            "Where exactly did you lose/find it?"
        ],
        "meeting_arrangements": [
            "Can we meet at a public place like a shopping center?",
            "I'm available this weekend. What works for you?",
            "Let's meet at the police station for safety.",
            "Can we meet during daytime hours?"
        ]
    }