from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_, or_
from typing import List, Optional
from datetime import datetime, timedelta
from ..core.database import get_db
from ..models.enhanced_models import (
    User, Item, Match, Message, Payment, Commission, Review, 
    Notification, AuditLog, SystemSettings, UserRole, ItemStatus, PaymentStatus
)
from ..models.enhanced_schemas import (
    AdminStats, AdminUserResponse, CommissionResponse, PaymentResponse
)
from ..services.enhanced_matching import EnhancedMatchingService
from ..services.payment_service import PaymentService
from .auth import get_current_user
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/admin", tags=["admin"])

def verify_admin(current_user: User = Depends(get_current_user)):
    """Verify user has admin privileges"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

@router.get("/stats", response_model=AdminStats)
def get_admin_stats(
    db: Session = Depends(get_db),
    admin_user: User = Depends(verify_admin)
):
    """Get comprehensive system statistics"""
    try:
        # Basic counts
        total_users = db.query(User).count()
        total_items = db.query(Item).filter(Item.is_active == True).count()
        total_lost_items = db.query(Item).filter(
            and_(Item.status == ItemStatus.LOST, Item.is_active == True)
        ).count()
        total_found_items = db.query(Item).filter(
            and_(Item.status == ItemStatus.FOUND, Item.is_active == True)
        ).count()
        total_recovered_items = db.query(Item).filter(
            Item.status == ItemStatus.RECOVERED
        ).count()
        
        # Matching stats
        total_matches = db.query(Match).count()
        total_messages = db.query(Message).count()
        
        # Payment stats
        total_payments = db.query(func.sum(Payment.amount)).filter(
            Payment.status == PaymentStatus.COMPLETED
        ).scalar() or 0
        
        total_commissions = db.query(func.sum(Commission.amount)).scalar() or 0
        
        # Today's activity
        today = datetime.utcnow().date()
        active_users_today = db.query(User).filter(
            func.date(User.last_login) == today
        ).count()
        
        new_items_today = db.query(Item).filter(
            func.date(Item.created_at) == today
        ).count()
        
        successful_recoveries_today = db.query(Item).filter(
            and_(
                Item.status == ItemStatus.RECOVERED,
                func.date(Item.updated_at) == today
            )
        ).count()
        
        return AdminStats(
            total_users=total_users,
            total_items=total_items,
            total_lost_items=total_lost_items,
            total_found_items=total_found_items,
            total_recovered_items=total_recovered_items,
            total_matches=total_matches,
            total_messages=total_messages,
            total_payments=total_payments,
            total_commissions=total_commissions,
            active_users_today=active_users_today,
            new_items_today=new_items_today,
            successful_recoveries_today=successful_recoveries_today
        )
        
    except Exception as e:
        logger.error(f"Error getting admin stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve statistics")

@router.get("/users", response_model=List[AdminUserResponse])
def get_all_users(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    search: Optional[str] = None,
    role: Optional[UserRole] = None,
    is_active: Optional[bool] = None,
    sort_by: str = Query("created_at", regex="^(created_at|last_login|email|full_name)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db),
    admin_user: User = Depends(verify_admin)
):
    """Get all users with filtering and pagination"""
    try:
        query = db.query(User)
        
        # Apply filters
        if search:
            query = query.filter(
                or_(
                    User.full_name.ilike(f"%{search}%"),
                    User.email.ilike(f"%{search}%"),
                    User.phone.ilike(f"%{search}%")
                )
            )
        
        if role:
            query = query.filter(User.role == role)
        
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        # Apply sorting
        if sort_by == "created_at":
            order_col = User.created_at
        elif sort_by == "last_login":
            order_col = User.last_login
        elif sort_by == "email":
            order_col = User.email
        elif sort_by == "full_name":
            order_col = User.full_name
        
        if sort_order == "desc":
            query = query.order_by(desc(order_col))
        else:
            query = query.order_by(order_col)
        
        # Apply pagination
        offset = (page - 1) * per_page
        users = query.offset(offset).limit(per_page).all()
        
        return users
        
    except Exception as e:
        logger.error(f"Error getting users: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve users")

@router.put("/users/{user_id}/toggle-active")
def toggle_user_active(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(verify_admin)
):
    """Toggle user active status"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Don't allow deactivating other admins
        if user.role == UserRole.ADMIN and user.id != admin_user.id:
            raise HTTPException(status_code=403, detail="Cannot deactivate other admin users")
        
        user.is_active = not user.is_active
        db.commit()
        
        # Log the action
        audit_log = AuditLog(
            user_id=admin_user.id,
            action="toggle_user_active",
            resource_type="user",
            resource_id=user_id,
            details={"new_status": user.is_active}
        )
        db.add(audit_log)
        db.commit()
        
        return {
            "message": f"User {'activated' if user.is_active else 'deactivated'} successfully",
            "user_id": user_id,
            "is_active": user.is_active
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error toggling user active status: {e}")
        raise HTTPException(status_code=500, detail="Failed to update user status")

@router.put("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    new_role: UserRole,
    db: Session = Depends(get_db),
    admin_user: User = Depends(verify_admin)
):
    """Update user role"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        old_role = user.role
        user.role = new_role
        db.commit()
        
        # Log the action
        audit_log = AuditLog(
            user_id=admin_user.id,
            action="update_user_role",
            resource_type="user",
            resource_id=user_id,
            details={"old_role": old_role, "new_role": new_role}
        )
        db.add(audit_log)
        db.commit()
        
        return {
            "message": "User role updated successfully",
            "user_id": user_id,
            "old_role": old_role,
            "new_role": new_role
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user role: {e}")
        raise HTTPException(status_code=500, detail="Failed to update user role")

@router.get("/items")
def get_all_items(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    status: Optional[ItemStatus] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    db: Session = Depends(get_db),
    admin_user: User = Depends(verify_admin)
):
    """Get all items with admin filtering"""
    try:
        query = db.query(Item)
        
        # Apply filters
        if status:
            query = query.filter(Item.status == status)
        
        if category:
            query = query.filter(Item.category == category)
        
        if search:
            query = query.filter(
                or_(
                    Item.title.ilike(f"%{search}%"),
                    Item.description.ilike(f"%{search}%"),
                    Item.brand.ilike(f"%{search}%")
                )
            )
        
        if date_from:
            query = query.filter(Item.created_at >= date_from)
        
        if date_to:
            query = query.filter(Item.created_at <= date_to)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * per_page
        items = query.order_by(desc(Item.created_at)).offset(offset).limit(per_page).all()
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "per_page": per_page,
            "has_next": (page * per_page) < total,
            "has_prev": page > 1
        }
        
    except Exception as e:
        logger.error(f"Error getting items: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve items")

@router.put("/items/{item_id}/feature")
def toggle_item_featured(
    item_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(verify_admin)
):
    """Toggle item featured status"""
    try:
        item = db.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        item.is_featured = not item.is_featured
        db.commit()
        
        # Log the action
        audit_log = AuditLog(
            user_id=admin_user.id,
            action="toggle_item_featured",
            resource_type="item",
            resource_id=item_id,
            details={"is_featured": item.is_featured}
        )
        db.add(audit_log)
        db.commit()
        
        return {
            "message": f"Item {'featured' if item.is_featured else 'unfeatured'} successfully",
            "item_id": item_id,
            "is_featured": item.is_featured
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error toggling item featured status: {e}")
        raise HTTPException(status_code=500, detail="Failed to update item status")

@router.get("/payments", response_model=List[PaymentResponse])
def get_all_payments(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    status: Optional[PaymentStatus] = None,
    payment_method: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    db: Session = Depends(get_db),
    admin_user: User = Depends(verify_admin)
):
    """Get all payments with filtering"""
    try:
        query = db.query(Payment)
        
        # Apply filters
        if status:
            query = query.filter(Payment.status == status)
        
        if payment_method:
            query = query.filter(Payment.payment_method == payment_method)
        
        if date_from:
            query = query.filter(Payment.created_at >= date_from)
        
        if date_to:
            query = query.filter(Payment.created_at <= date_to)
        
        # Apply pagination
        offset = (page - 1) * per_page
        payments = query.order_by(desc(Payment.created_at)).offset(offset).limit(per_page).all()
        
        return payments
        
    except Exception as e:
        logger.error(f"Error getting payments: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve payments")

@router.get("/commissions", response_model=List[CommissionResponse])
def get_all_commissions(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    admin_user: User = Depends(verify_admin)
):
    """Get all commissions"""
    try:
        query = db.query(Commission)
        
        if status:
            query = query.filter(Commission.status == status)
        
        offset = (page - 1) * per_page
        commissions = query.order_by(desc(Commission.created_at)).offset(offset).limit(per_page).all()
        
        return commissions
        
    except Exception as e:
        logger.error(f"Error getting commissions: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve commissions")

@router.put("/commissions/{commission_id}/mark-paid")
def mark_commission_paid(
    commission_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(verify_admin)
):
    """Mark commission as paid"""
    try:
        commission = db.query(Commission).filter(Commission.id == commission_id).first()
        if not commission:
            raise HTTPException(status_code=404, detail="Commission not found")
        
        commission.status = "paid"
        commission.paid_at = datetime.utcnow()
        db.commit()
        
        # Log the action
        audit_log = AuditLog(
            user_id=admin_user.id,
            action="mark_commission_paid",
            resource_type="commission",
            resource_id=commission_id,
            details={"amount": commission.amount}
        )
        db.add(audit_log)
        db.commit()
        
        return {
            "message": "Commission marked as paid",
            "commission_id": commission_id,
            "amount": commission.amount
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error marking commission as paid: {e}")
        raise HTTPException(status_code=500, detail="Failed to update commission")

@router.post("/payments/{payment_id}/refund")
def refund_payment(
    payment_id: int,
    reason: str,
    db: Session = Depends(get_db),
    admin_user: User = Depends(verify_admin)
):
    """Refund a payment"""
    try:
        payment_service = PaymentService(db)
        result = payment_service.refund_payment(payment_id, reason)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        
        # Log the action
        audit_log = AuditLog(
            user_id=admin_user.id,
            action="refund_payment",
            resource_type="payment",
            resource_id=payment_id,
            details={"reason": reason}
        )
        db.add(audit_log)
        db.commit()
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error refunding payment: {e}")
        raise HTTPException(status_code=500, detail="Failed to process refund")

@router.get("/matching/stats")
def get_matching_stats(
    db: Session = Depends(get_db),
    admin_user: User = Depends(verify_admin)
):
    """Get AI matching performance statistics"""
    try:
        matching_service = EnhancedMatchingService(db)
        stats = matching_service.get_matching_statistics()
        
        return stats
        
    except Exception as e:
        logger.error(f"Error getting matching stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve matching statistics")

@router.post("/matching/bulk-rematch")
def bulk_rematch_items(
    status: Optional[ItemStatus] = None,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    admin_user: User = Depends(verify_admin)
):
    """Bulk rematch items (useful after algorithm improvements)"""
    try:
        matching_service = EnhancedMatchingService(db)
        matching_service.bulk_rematch_items(status, limit)
        
        # Log the action
        audit_log = AuditLog(
            user_id=admin_user.id,
            action="bulk_rematch",
            resource_type="system",
            details={"status": status, "limit": limit}
        )
        db.add(audit_log)
        db.commit()
        
        return {
            "message": f"Bulk rematch initiated for up to {limit} items",
            "status_filter": status
        }
        
    except Exception as e:
        logger.error(f"Error in bulk rematch: {e}")
        raise HTTPException(status_code=500, detail="Failed to initiate bulk rematch")

@router.get("/audit-logs")
def get_audit_logs(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    action: Optional[str] = None,
    user_id: Optional[int] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    db: Session = Depends(get_db),
    admin_user: User = Depends(verify_admin)
):
    """Get system audit logs"""
    try:
        query = db.query(AuditLog)
        
        # Apply filters
        if action:
            query = query.filter(AuditLog.action == action)
        
        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        
        if date_from:
            query = query.filter(AuditLog.created_at >= date_from)
        
        if date_to:
            query = query.filter(AuditLog.created_at <= date_to)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * per_page
        logs = query.order_by(desc(AuditLog.created_at)).offset(offset).limit(per_page).all()
        
        return {
            "logs": logs,
            "total": total,
            "page": page,
            "per_page": per_page
        }
        
    except Exception as e:
        logger.error(f"Error getting audit logs: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve audit logs")

@router.get("/system-settings")
def get_system_settings(
    db: Session = Depends(get_db),
    admin_user: User = Depends(verify_admin)
):
    """Get system settings"""
    try:
        settings = db.query(SystemSettings).all()
        
        return {
            setting.key: {
                "value": setting.value,
                "description": setting.description,
                "updated_at": setting.updated_at
            }
            for setting in settings
        }
        
    except Exception as e:
        logger.error(f"Error getting system settings: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve system settings")

@router.put("/system-settings/{key}")
def update_system_setting(
    key: str,
    value: str,
    description: Optional[str] = None,
    db: Session = Depends(get_db),
    admin_user: User = Depends(verify_admin)
):
    """Update a system setting"""
    try:
        setting = db.query(SystemSettings).filter(SystemSettings.key == key).first()
        
        if setting:
            old_value = setting.value
            setting.value = value
            if description:
                setting.description = description
            setting.updated_at = datetime.utcnow()
        else:
            setting = SystemSettings(
                key=key,
                value=value,
                description=description or f"Setting for {key}"
            )
            db.add(setting)
            old_value = None
        
        db.commit()
        
        # Log the action
        audit_log = AuditLog(
            user_id=admin_user.id,
            action="update_system_setting",
            resource_type="system_setting",
            details={"key": key, "old_value": old_value, "new_value": value}
        )
        db.add(audit_log)
        db.commit()
        
        return {
            "message": "System setting updated successfully",
            "key": key,
            "value": value
        }
        
    except Exception as e:
        logger.error(f"Error updating system setting: {e}")
        raise HTTPException(status_code=500, detail="Failed to update system setting")

@router.get("/dashboard-data")
def get_dashboard_data(
    db: Session = Depends(get_db),
    admin_user: User = Depends(verify_admin)
):
    """Get comprehensive dashboard data"""
    try:
        # Recent activity (last 7 days)
        week_ago = datetime.utcnow() - timedelta(days=7)
        
        recent_users = db.query(User).filter(User.created_at >= week_ago).count()
        recent_items = db.query(Item).filter(Item.created_at >= week_ago).count()
        recent_matches = db.query(Match).filter(Match.created_at >= week_ago).count()
        recent_payments = db.query(Payment).filter(
            and_(
                Payment.created_at >= week_ago,
                Payment.status == PaymentStatus.COMPLETED
            )
        ).count()
        
        # Top categories
        top_categories = db.query(
            Item.category,
            func.count(Item.id).label('count')
        ).filter(Item.is_active == True).group_by(Item.category).order_by(desc('count')).limit(5).all()
        
        # Payment method distribution
        payment_methods = db.query(
            Payment.payment_method,
            func.count(Payment.id).label('count'),
            func.sum(Payment.amount).label('total_amount')
        ).filter(Payment.status == PaymentStatus.COMPLETED).group_by(Payment.payment_method).all()
        
        return {
            "recent_activity": {
                "new_users": recent_users,
                "new_items": recent_items,
                "new_matches": recent_matches,
                "completed_payments": recent_payments
            },
            "top_categories": [
                {"category": cat.category, "count": cat.count}
                for cat in top_categories
            ],
            "payment_methods": [
                {
                    "method": pm.payment_method,
                    "count": pm.count,
                    "total_amount": pm.total_amount
                }
                for pm in payment_methods
            ]
        }
        
    except Exception as e:
        logger.error(f"Error getting dashboard data: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve dashboard data")