from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.database import get_db
from ..models.enhanced_models import Payment, PaymentStatus, User, Item
from ..models.enhanced_schemas import PaymentCreate, PaymentResponse, PaymentInitiate
from ..services.payment_service import PaymentService
from .auth import get_current_user
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/initiate", response_model=dict)
def initiate_payment(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Initiate a payment to unlock contact information"""
    try:
        payment_service = PaymentService(db)
        result = payment_service.initiate_payment(current_user.id, payment_data)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        
        return {
            "success": True,
            "message": "Payment initiated successfully",
            "data": {
                "payment_id": result["payment_id"],
                "transaction_id": result["transaction_id"],
                "instructions": result["instructions"],
                "payment_url": result.get("payment_url"),
                "qr_code": result.get("qr_code")
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error initiating payment: {e}")
        raise HTTPException(status_code=500, detail="Payment initiation failed")

@router.get("/verify/{payment_id}")
def verify_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Verify payment status"""
    try:
        # Check if user owns this payment
        payment = db.query(Payment).filter(
            Payment.id == payment_id,
            Payment.user_id == current_user.id
        ).first()
        
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        payment_service = PaymentService(db)
        result = payment_service.verify_payment(payment_id)
        
        return {
            "success": result["success"],
            "status": result.get("status", "unknown"),
            "message": result["message"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error verifying payment {payment_id}: {e}")
        raise HTTPException(status_code=500, detail="Payment verification failed")

@router.get("/contact/{item_id}")
def get_contact_info(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get contact information after successful payment"""
    try:
        payment_service = PaymentService(db)
        result = payment_service.get_contact_info(current_user.id, item_id)
        
        if not result["success"]:
            raise HTTPException(status_code=403, detail=result["message"])
        
        return {
            "success": True,
            "data": {
                "owner_name": result["owner_name"],
                "phone": result.get("phone"),
                "email": result.get("email"),
                "contact_method": result["contact_method"],
                "instructions": result["instructions"]
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting contact info for item {item_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve contact information")

@router.get("/my-payments", response_model=List[PaymentResponse])
def get_my_payments(
    limit: int = Query(50, ge=1, le=100),
    status: Optional[PaymentStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's payment history"""
    try:
        query = db.query(Payment).filter(Payment.user_id == current_user.id)
        
        if status:
            query = query.filter(Payment.status == status)
        
        payments = query.order_by(Payment.created_at.desc()).limit(limit).all()
        
        return payments
        
    except Exception as e:
        logger.error(f"Error getting user payments: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve payments")

@router.get("/check-access/{item_id}")
def check_payment_access(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Check if user has paid for access to an item's contact info"""
    try:
        # Check if user has completed payment for this item
        payment = db.query(Payment).filter(
            Payment.user_id == current_user.id,
            Payment.item_id == item_id,
            Payment.status == PaymentStatus.COMPLETED
        ).first()
        
        has_access = payment is not None
        
        # Get item info
        item = db.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        return {
            "has_access": has_access,
            "payment_required": not has_access,
            "unlock_fee": 1000.0,  # 1,000 RWF
            "currency": "RWF",
            "item_title": item.title,
            "item_status": item.status,
            "payment_id": payment.id if payment else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error checking payment access for item {item_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to check payment access")

@router.post("/simulate-completion/{payment_id}")
def simulate_payment_completion(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Simulate payment completion (for testing purposes)"""
    try:
        # Check if user owns this payment
        payment = db.query(Payment).filter(
            Payment.id == payment_id,
            Payment.user_id == current_user.id
        ).first()
        
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        payment_service = PaymentService(db)
        result = payment_service.simulate_payment_completion(payment_id)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        
        return {
            "success": True,
            "message": "Payment completed successfully (simulated)",
            "payment_id": payment_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error simulating payment completion: {e}")
        raise HTTPException(status_code=500, detail="Simulation failed")

@router.get("/methods")
def get_payment_methods():
    """Get available payment methods"""
    return {
        "methods": [
            {
                "id": "mtn_momo",
                "name": "MTN Mobile Money",
                "description": "Pay instantly using MTN Mobile Money",
                "icon": "📱",
                "requires_phone": True,
                "processing_time": "Instant (5-30 seconds)",
                "fees": "No additional fees",
                "enabled": True
            }
        ],
        "note": "Only MTN Mobile Money is currently supported.",
        "unlock_fee": 1000.0,
        "currency": "RWF",
        "commission_rate": 0.10
    }

@router.get("/receipt/{payment_id}")
def get_payment_receipt(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get payment receipt"""
    try:
        payment = db.query(Payment).filter(
            Payment.id == payment_id,
            Payment.user_id == current_user.id
        ).first()
        
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        # Get item info
        item = db.query(Item).filter(Item.id == payment.item_id).first()
        
        return {
            "payment_id": payment.id,
            "transaction_id": payment.transaction_id,
            "amount": payment.amount,
            "currency": payment.currency,
            "payment_method": payment.payment_method,
            "status": payment.status,
            "description": payment.description,
            "created_at": payment.created_at,
            "completed_at": payment.completed_at,
            "item": {
                "id": item.id,
                "title": item.title,
                "status": item.status,
                "category": item.category
            } if item else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting payment receipt: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve receipt")

@router.post("/request-refund/{payment_id}")
def request_refund(
    payment_id: int,
    reason: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Request a refund for a payment"""
    try:
        payment = db.query(Payment).filter(
            Payment.id == payment_id,
            Payment.user_id == current_user.id,
            Payment.status == PaymentStatus.COMPLETED
        ).first()
        
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found or not eligible for refund")
        
        # In a real system, this would create a refund request for admin review
        # For now, we'll just log the request
        logger.info(f"Refund requested for payment {payment_id} by user {current_user.id}: {reason}")
        
        return {
            "success": True,
            "message": "Refund request submitted successfully. It will be reviewed by our team within 24 hours.",
            "request_id": f"REF_{payment_id}_{current_user.id}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error requesting refund: {e}")
        raise HTTPException(status_code=500, detail="Failed to submit refund request")

@router.get("/stats")
def get_payment_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's payment statistics"""
    try:
        total_payments = db.query(Payment).filter(Payment.user_id == current_user.id).count()
        completed_payments = db.query(Payment).filter(
            Payment.user_id == current_user.id,
            Payment.status == PaymentStatus.COMPLETED
        ).count()
        
        total_spent = db.query(func.sum(Payment.amount)).filter(
            Payment.user_id == current_user.id,
            Payment.status == PaymentStatus.COMPLETED
        ).scalar() or 0
        
        return {
            "total_payments": total_payments,
            "completed_payments": completed_payments,
            "pending_payments": total_payments - completed_payments,
            "total_spent": total_spent,
            "currency": "RWF",
            "contacts_unlocked": completed_payments
        }
        
    except Exception as e:
        logger.error(f"Error getting payment stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve payment statistics")