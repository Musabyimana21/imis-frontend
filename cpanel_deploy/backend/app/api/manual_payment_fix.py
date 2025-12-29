"""Manual Payment Verification - WORKING SOLUTION"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models.enhanced_models import Payment, PaymentStatus, User
from ..models.enhanced_schemas import PaymentCreate
from .auth import get_current_user
import uuid
from datetime import datetime

router = APIRouter(prefix="/payments/manual", tags=["manual-payments"])

@router.post("/initiate-manual")
def initiate_manual_payment(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Initiate manual payment - USER PAYS VIA MTN APP"""
    
    # Create payment record
    payment = Payment(
        user_id=current_user.id,
        item_id=payment_data.item_id,
        amount=payment_data.amount,
        payment_method="mtn_momo_manual",
        phone_number=payment_data.phone_number,
        description=f"Manual payment for item {payment_data.item_id}",
        transaction_id=f"MANUAL_{uuid.uuid4().hex[:12].upper()}",
        status=PaymentStatus.PENDING
    )
    
    db.add(payment)
    db.commit()
    db.refresh(payment)
    
    return {
        "success": True,
        "payment_id": payment.id,
        "transaction_id": payment.transaction_id,
        "instructions": f"""
MANUAL PAYMENT INSTRUCTIONS:

1. Open your MTN Mobile Money app
2. Send 1,000 RWF to: 250796888309
3. Use reference: {payment.transaction_id}
4. After sending, enter the MTN transaction reference below
5. Admin will verify and unlock contact

Merchant: IMS.SP
Amount: 1,000 RWF
Your Reference: {payment.transaction_id}
        """,
        "merchant_phone": "250796888309",
        "amount": 1000
    }

@router.post("/submit-reference/{payment_id}")
def submit_payment_reference(
    payment_id: int,
    mtn_reference: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """User submits MTN transaction reference after paying"""
    
    payment = db.query(Payment).filter(
        Payment.id == payment_id,
        Payment.user_id == current_user.id
    ).first()
    
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    # Store MTN reference
    payment.external_reference = mtn_reference
    payment.description = f"{payment.description} | MTN Ref: {mtn_reference}"
    db.commit()
    
    return {
        "success": True,
        "message": "Reference submitted. Admin will verify within 5 minutes.",
        "payment_id": payment_id,
        "status": "pending_verification"
    }

@router.post("/admin/verify/{payment_id}")
def admin_verify_payment(
    payment_id: int,
    approved: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Admin verifies manual payment"""
    
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin only")
    
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    if approved:
        payment.status = PaymentStatus.COMPLETED
        payment.completed_at = datetime.utcnow()
        message = "Payment verified and approved"
    else:
        payment.status = PaymentStatus.FAILED
        message = "Payment rejected"
    
    db.commit()
    
    return {
        "success": True,
        "message": message,
        "payment_id": payment_id
    }
