from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from typing import List, Optional
from datetime import datetime, timedelta
from ..core.database import get_db
from ..models.enhanced_models import Item, User, Match, ItemStatus, ItemCategory
from ..models.enhanced_schemas import (
    ItemCreate, ItemUpdate, ItemResponse, ItemSummary, 
    MatchResponse, MatchSummary, ItemSearchFilters, SearchResponse
)
from ..services.enhanced_matching import EnhancedMatchingService
from .auth import get_current_user, get_current_user_optional
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/items", tags=["items"])

@router.post("/", response_model=ItemResponse)
def create_item(
    item: ItemCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Create a new lost or found item"""
    try:
        # Create item
        db_item = Item(
            user_id=current_user.id,
            title=item.title,
            description=item.description,
            category=item.category,
            status=item.status,
            location_name=item.location_name,
            latitude=item.latitude,
            longitude=item.longitude,
            date_lost_found=item.date_lost_found,
            brand=item.brand,
            model=item.model,
            color=item.color,
            size=item.size,
            distinctive_features=item.distinctive_features,
            reward_amount=item.reward_amount or 0.0,
            contact_method=item.contact_method,
            allow_public_contact=item.allow_public_contact
        )
        
        # Generate text vector for search optimization
        text_content = f"{item.title} {item.description} {item.brand or ''} {item.model or ''} {item.color or ''}"
        db_item.text_vector = text_content.lower()
        
        # Extract keywords
        keywords = list(set(text_content.lower().split()))
        db_item.match_keywords = keywords[:20]  # Limit to 20 keywords
        
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        
        # Update user statistics
        if item.status == ItemStatus.LOST:
            current_user.items_lost += 1
        else:
            current_user.items_found += 1
        db.commit()
        
        # Find matches using enhanced AI
        matching_service = EnhancedMatchingService(db)
        matches = matching_service.find_matches(db_item.id)
        
        logger.info(f"Created item {db_item.id} with {len(matches)} matches")
        
        return db_item
        
    except Exception as e:
        logger.error(f"Error creating item: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create item")

@router.get("/", response_model=SearchResponse)
def get_items(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    category: Optional[ItemCategory] = None,
    status: Optional[ItemStatus] = None,
    location: Optional[str] = None,
    radius_km: Optional[float] = Query(None, ge=1, le=200),
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    has_reward: Optional[bool] = None,
    min_reward: Optional[float] = None,
    max_reward: Optional[float] = None,
    search: Optional[str] = None,
    sort_by: str = Query("created_at", regex="^(created_at|reward_amount|distance)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    user_lat: Optional[float] = None,
    user_lon: Optional[float] = None,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Get items with advanced filtering and search"""
    try:
        # Base query
        query = db.query(Item).filter(Item.is_active == True)
        
        # Apply filters
        if category:
            query = query.filter(Item.category == category)
        
        if status:
            query = query.filter(Item.status == status)
        
        if location:
            query = query.filter(Item.location_name.ilike(f"%{location}%"))
        
        if date_from:
            query = query.filter(Item.date_lost_found >= date_from)
        
        if date_to:
            query = query.filter(Item.date_lost_found <= date_to)
        
        if has_reward is not None:
            if has_reward:
                query = query.filter(Item.reward_amount > 0)
            else:
                query = query.filter(Item.reward_amount == 0)
        
        if min_reward is not None:
            query = query.filter(Item.reward_amount >= min_reward)
        
        if max_reward is not None:
            query = query.filter(Item.reward_amount <= max_reward)
        
        # Text search
        if search:
            search_terms = search.lower().split()
            for term in search_terms:
                query = query.filter(
                    or_(
                        Item.title.ilike(f"%{term}%"),
                        Item.description.ilike(f"%{term}%"),
                        Item.brand.ilike(f"%{term}%"),
                        Item.model.ilike(f"%{term}%"),
                        Item.color.ilike(f"%{term}%")
                    )
                )
        
        # Location-based filtering
        if radius_km and user_lat and user_lon:
            # This is a simplified distance filter
            # In production, you'd use PostGIS for accurate distance calculation
            lat_range = radius_km / 111.0  # Rough conversion
            lon_range = radius_km / (111.0 * abs(user_lat))
            
            query = query.filter(
                and_(
                    Item.latitude.between(user_lat - lat_range, user_lat + lat_range),
                    Item.longitude.between(user_lon - lon_range, user_lon + lon_range)
                )
            )
        
        # Get total count
        total = query.count()
        
        # Apply sorting
        if sort_by == "created_at":
            if sort_order == "desc":
                query = query.order_by(desc(Item.created_at))
            else:
                query = query.order_by(Item.created_at)
        elif sort_by == "reward_amount":
            if sort_order == "desc":
                query = query.order_by(desc(Item.reward_amount))
            else:
                query = query.order_by(Item.reward_amount)
        
        # Apply pagination
        offset = (page - 1) * per_page
        items = query.offset(offset).limit(per_page).all()
        
        # Calculate distance if user location provided
        if user_lat and user_lon:
            for item in items:
                # Simple distance calculation (replace with PostGIS in production)
                import math
                R = 6371  # Earth radius in km
                lat1, lon1 = math.radians(user_lat), math.radians(user_lon)
                lat2, lon2 = math.radians(item.latitude), math.radians(item.longitude)
                dlat, dlon = lat2 - lat1, lon2 - lon1
                a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
                c = 2 * math.asin(math.sqrt(a))
                item.distance_km = R * c
        
        return SearchResponse(
            items=items,
            total=total,
            page=page,
            per_page=per_page,
            has_next=(page * per_page) < total,
            has_prev=page > 1
        )
        
    except Exception as e:
        logger.error(f"Error getting items: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve items")

@router.get("/{item_id}", response_model=ItemResponse)
def get_item(
    item_id: int, 
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Get a specific item by ID"""
    item = db.query(Item).filter(Item.id == item_id, Item.is_active == True).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Increment view count
    item.view_count += 1
    db.commit()
    
    return item

@router.put("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int,
    item_update: ItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an item (only by owner)"""
    item = db.query(Item).filter(
        Item.id == item_id,
        Item.user_id == current_user.id,
        Item.is_active == True
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found or not authorized")
    
    # Update fields
    update_data = item_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    
    item.updated_at = datetime.utcnow()
    
    # Update text vector if content changed
    if any(field in update_data for field in ['title', 'description', 'brand', 'model', 'color']):
        text_content = f"{item.title} {item.description} {item.brand or ''} {item.model or ''} {item.color or ''}"
        item.text_vector = text_content.lower()
        
        # Re-run matching if significant changes
        matching_service = EnhancedMatchingService(db)
        matching_service.find_matches(item.id, force_refresh=True)
    
    db.commit()
    db.refresh(item)
    
    return item

@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Soft delete an item (only by owner)"""
    item = db.query(Item).filter(
        Item.id == item_id,
        Item.user_id == current_user.id
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found or not authorized")
    
    item.is_active = False
    db.commit()
    
    return {"message": "Item deleted successfully"}

@router.get("/{item_id}/matches", response_model=List[MatchSummary])
def get_item_matches(
    item_id: int,
    limit: int = Query(10, ge=1, le=50),
    confidence: Optional[str] = Query(None, regex="^(low|medium|high)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get matches for an item (only by owner)"""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Check if user owns the item or is admin
    if item.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to view matches")
    
    # Get matches
    query = db.query(Match).filter(
        Match.item_id == item_id,
        Match.is_dismissed == False
    )
    
    if confidence:
        query = query.filter(Match.confidence_level == confidence)
    
    matches = query.order_by(desc(Match.similarity_score)).limit(limit).all()
    
    return matches

@router.post("/{item_id}/matches/{match_id}/confirm")
def confirm_match(
    item_id: int,
    match_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Confirm a match"""
    matching_service = EnhancedMatchingService(db)
    success = matching_service.confirm_match(match_id, current_user.id)
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to confirm match")
    
    return {"message": "Match confirmed successfully"}

@router.post("/{item_id}/matches/{match_id}/dismiss")
def dismiss_match(
    item_id: int,
    match_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Dismiss a match"""
    matching_service = EnhancedMatchingService(db)
    success = matching_service.dismiss_match(match_id, current_user.id)
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to dismiss match")
    
    return {"message": "Match dismissed successfully"}

@router.post("/{item_id}/rematch")
def rematch_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Force rematch for an item (owner or admin only)"""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Check authorization
    if item.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    matching_service = EnhancedMatchingService(db)
    matches = matching_service.find_matches(item_id, force_refresh=True)
    
    return {
        "message": "Rematch completed successfully",
        "matches_found": len(matches)
    }

@router.post("/{item_id}/mark-recovered")
def mark_item_recovered(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark an item as recovered"""
    item = db.query(Item).filter(
        Item.id == item_id,
        Item.user_id == current_user.id
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found or not authorized")
    
    item.status = ItemStatus.RECOVERED
    item.updated_at = datetime.utcnow()
    
    # Update user statistics
    current_user.items_recovered += 1
    
    db.commit()
    
    return {"message": "Item marked as recovered successfully"}

@router.get("/{item_id}/similar", response_model=List[ItemSummary])
def get_similar_items(
    item_id: int,
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """Get similar items (public endpoint)"""
    item = db.query(Item).filter(Item.id == item_id, Item.is_active == True).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Find similar items based on category and location
    similar_items = db.query(Item).filter(
        and_(
            Item.id != item_id,
            Item.category == item.category,
            Item.is_active == True,
            # Simple location filter (within ~50km)
            Item.latitude.between(item.latitude - 0.5, item.latitude + 0.5),
            Item.longitude.between(item.longitude - 0.5, item.longitude + 0.5)
        )
    ).order_by(desc(Item.created_at)).limit(limit).all()
    
    return similar_items

@router.get("/categories/stats")
def get_category_stats(db: Session = Depends(get_db)):
    """Get statistics by category"""
    stats = db.query(
        Item.category,
        func.count(Item.id).label('total'),
        func.sum(func.case([(Item.status == ItemStatus.LOST, 1)], else_=0)).label('lost'),
        func.sum(func.case([(Item.status == ItemStatus.FOUND, 1)], else_=0)).label('found'),
        func.sum(func.case([(Item.status == ItemStatus.RECOVERED, 1)], else_=0)).label('recovered')
    ).filter(Item.is_active == True).group_by(Item.category).all()
    
    return [
        {
            "category": stat.category,
            "total": stat.total,
            "lost": stat.lost or 0,
            "found": stat.found or 0,
            "recovered": stat.recovered or 0
        }
        for stat in stats
    ]

@router.post("/{item_id}/upload-image")
async def upload_item_image(
    item_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload an image for an item"""
    item = db.query(Item).filter(
        Item.id == item_id,
        Item.user_id == current_user.id
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found or not authorized")
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # In production, you would upload to cloud storage (AWS S3, Cloudinary, etc.)
    # For now, we'll just return a placeholder URL
    image_url = f"/api/images/{item_id}_{file.filename}"
    
    # Update item image URLs
    if not item.image_urls:
        item.image_urls = []
    
    item.image_urls.append(image_url)
    
    # Set as primary image if it's the first one
    if not item.primary_image_url or item.primary_image_url == "/api/placeholder/400/300":
        item.primary_image_url = image_url
    
    db.commit()
    
    return {
        "message": "Image uploaded successfully",
        "image_url": image_url
    }