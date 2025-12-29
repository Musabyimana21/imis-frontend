from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from ..core.database import get_db
from ..models.enhanced_models import User, Item, Commission, UserRole
from ..models.schemas import CommissionResponse
from .auth import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

@router.get("/stats")
def get_stats(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    return {
        "total_users": db.query(func.count(User.id)).scalar(),
        "total_items": db.query(func.count(Item.id)).scalar(),
        "lost_items": db.query(func.count(Item.id)).filter(Item.status == "lost").scalar(),
        "found_items": db.query(func.count(Item.id)).filter(Item.status == "found").scalar(),
        "recovered_items": db.query(func.count(Item.id)).filter(Item.status == "recovered").scalar(),
        "total_commissions": db.query(func.sum(Commission.amount)).scalar() or 0
    }

@router.get("/commissions", response_model=List[CommissionResponse])
def get_commissions(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    return db.query(Commission).all()

@router.post("/commissions/{item_id}")
def create_commission(item_id: int, amount: float, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    commission = Commission(
        item_id=item_id,
        user_id=item.user_id,
        amount=amount,
        rate=0.10
    )
    db.add(commission)
    item.status = "recovered"
    db.commit()
    return {"message": "Commission created"}

@router.get("/users")
def get_users(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    return db.query(User).all()
