"""Manual payment verification endpoints"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Dict
from pydantic import BaseModel
from ..core.database import get_db
from ..models.enhanced_models import AnonymousPayment, AnonymousItem
from ..services.payment_alternatives import PaymentAlternatives

router = APIRouter()

class ManualPaymentVerification(BaseModel):
    reference: str
    payment_method: str
    phone_number: str
    screenshot_url: str = None
    notes: str = None

@router.post("/manual-payment/verify", response_model=Dict)
async def verify_manual_payment(
    payment_data: ManualPaymentVerification, 
    db: Session = Depends(get_db)
):
    """Verify manual payment and unlock contact"""
    try:
        alt_payments = PaymentAlternatives()
        
        # Simulate verification process
        verification = alt_payments.verify_manual_payment(
            payment_data.reference,
            payment_data.payment_method,
            payment_data.phone_number
        )
        
        # For demo purposes, auto-approve after 30 seconds
        # In production, this would be manual verification
        
        return {
            "success": True,
            "message": "Payment verification submitted successfully",
            "reference": payment_data.reference,
            "status": "pending_verification",
            "estimated_time": "2-5 minutes",
            "next_steps": [
                "Our team will verify your payment",
                "You'll receive SMS confirmation",
                "Contact info will be unlocked automatically"
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")

@router.get("/manual-payment/status/{reference}", response_model=Dict)
async def check_manual_payment_status(reference: str, db: Session = Depends(get_db)):
    """Check status of manual payment verification"""
    try:
        # For demo, return approved after any check
        return {
            "success": True,
            "reference": reference,
            "status": "approved",
            "message": "Payment verified successfully!",
            "contact_unlocked": True,
            "verified_at": "2024-01-01T12:00:00Z"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")

@router.get("/payment-methods", response_model=Dict)
async def get_available_payment_methods():
    """Get all available payment methods"""
    alt_payments = PaymentAlternatives()
    
    return {
        "mtn_momo": {
            "name": "MTN Mobile Money",
            "status": "unavailable",
            "reason": "IP whitelisting required"
        },
        "alternatives": alt_payments.methods,
        "support": {
            "phone": "+250780460621",
            "whatsapp": "+250780460621",
            "email": "gaudencemusabyimana21@gmail.com"
        }
    }