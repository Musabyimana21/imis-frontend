from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db

try:
    from geoalchemy2.functions import ST_GeogFromText
    HAS_POSTGIS = True
except ImportError:
    HAS_POSTGIS = False
from ..models.enhanced_models import Item, User
from ..models.schemas import ItemCreate, ItemResponse, MatchResponse
from ..services.matching import MatchingService
from .auth import get_current_user

router = APIRouter(prefix="/items", tags=["items"])

@router.post("/", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item_data = {
        'user_id': current_user.id,
        'title': item.title,
        'description': item.description,
        'category': item.category,
        'status': item.status,
        'location_name': item.location_name,
        'latitude': item.latitude,
        'longitude': item.longitude,
        'date_lost_found': item.date_lost_found
    }
    
    if HAS_POSTGIS:
        item_data['location'] = ST_GeogFromText(f'POINT({item.longitude} {item.latitude})')
    else:
        item_data['location'] = f'POINT({item.longitude} {item.latitude})'
    
    db_item = Item(**item_data)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    matching_service = MatchingService(db)
    matching_service.find_matches(db_item.id)
    
    return db_item

@router.get("/", response_model=List[ItemResponse])
def get_items(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(Item).filter(Item.is_active == True).offset(skip).limit(limit).all()

@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.get("/{item_id}/matches", response_model=List[MatchResponse])
def get_matches(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item.matches

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = db.query(Item).filter(Item.id == item_id, Item.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.is_active = False
    db.commit()
    return {"message": "Item deleted"}
