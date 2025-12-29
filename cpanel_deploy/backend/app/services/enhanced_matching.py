from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, or_
from ..models.enhanced_models import Item, Match, ItemStatus, ItemCategory, User, Notification
import math
import re
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
import logging

try:
    from geoalchemy2.functions import ST_Distance, ST_GeogFromText
    HAS_POSTGIS = True
except ImportError:
    HAS_POSTGIS = False

logger = logging.getLogger(__name__)

class EnhancedMatchingService:
    def __init__(self, db: Session):
        self.db = db
        self.text_weight = 0.7  # 70% text similarity
        self.location_weight = 0.3  # 30% location proximity
        self.max_distance_km = 50  # Maximum matching distance
        self.min_similarity_threshold = 0.3  # Minimum similarity to consider
        
    def calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity using TF-IDF and cosine similarity"""
        try:
            # Preprocess text
            text1_clean = self._preprocess_text(text1)
            text2_clean = self._preprocess_text(text2)
            
            if not text1_clean or not text2_clean:
                return 0.0
            
            # Use TF-IDF vectorization
            vectorizer = TfidfVectorizer(
                lowercase=True,
                stop_words='english',
                ngram_range=(1, 2),  # Include bigrams
                max_features=1000
            )
            
            tfidf_matrix = vectorizer.fit_transform([text1_clean, text2_clean])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity)
        except Exception as e:
            logger.error(f"Error calculating text similarity: {e}")
            return 0.0
    
    def _preprocess_text(self, text: str) -> str:
        """Clean and preprocess text for better matching"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points using Haversine formula"""
        if HAS_POSTGIS:
            try:
                # Use PostGIS for more accurate calculation
                point1 = f'POINT({lon1} {lat1})'
                point2 = f'POINT({lon2} {lat2})'
                distance = self.db.query(
                    func.ST_Distance(
                        ST_GeogFromText(point1),
                        ST_GeogFromText(point2)
                    )
                ).scalar()
                return distance / 1000 if distance else 999999  # Convert to km
            except Exception as e:
                logger.warning(f"PostGIS distance calculation failed: {e}")
        
        # Fallback to Haversine formula
        R = 6371  # Earth radius in kilometers
        
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = (math.sin(dlat/2)**2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2)
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    def calculate_category_bonus(self, cat1: ItemCategory, cat2: ItemCategory) -> float:
        """Calculate bonus score for category matching"""
        if cat1 == cat2:
            return 0.2  # 20% bonus for exact category match
        
        # Related categories get smaller bonus
        related_categories = {
            ItemCategory.PHONE: [ItemCategory.ELECTRONICS],
            ItemCategory.ELECTRONICS: [ItemCategory.PHONE],
            ItemCategory.WALLET: [ItemCategory.BAG],
            ItemCategory.BAG: [ItemCategory.WALLET],
        }
        
        if cat2 in related_categories.get(cat1, []):
            return 0.1  # 10% bonus for related categories
        
        return 0.0
    
    def calculate_brand_color_bonus(self, item1: Item, item2: Item) -> Tuple[float, bool, bool]:
        """Calculate bonus for brand and color matching"""
        brand_bonus = 0.0
        color_bonus = 0.0
        brand_match = False
        color_match = False
        
        # Brand matching
        if item1.brand and item2.brand:
            if item1.brand.lower() == item2.brand.lower():
                brand_bonus = 0.15  # 15% bonus for brand match
                brand_match = True
        
        # Color matching
        if item1.color and item2.color:
            if item1.color.lower() == item2.color.lower():
                color_bonus = 0.1  # 10% bonus for color match
                color_match = True
        
        return brand_bonus + color_bonus, brand_match, color_match
    
    def calculate_time_decay(self, item1_date: datetime, item2_date: datetime) -> float:
        """Apply time decay - items reported closer in time are more likely to match"""
        time_diff = abs((item1_date - item2_date).days)
        
        if time_diff <= 1:
            return 0.1  # 10% bonus for same day
        elif time_diff <= 7:
            return 0.05  # 5% bonus for same week
        elif time_diff <= 30:
            return 0.02  # 2% bonus for same month
        else:
            return -0.05  # Small penalty for older items
    
    def find_matches(self, item_id: int, force_refresh: bool = False) -> List[Dict]:
        """Find matches for a given item using enhanced AI algorithm"""
        try:
            item = self.db.query(Item).filter(Item.id == item_id).first()
            if not item:
                logger.error(f"Item {item_id} not found")
                return []
            
            # Clear existing matches if force refresh
            if force_refresh:
                self.db.query(Match).filter(Match.item_id == item_id).delete()
                self.db.commit()
            
            # Determine opposite status
            opposite_status = ItemStatus.FOUND if item.status == ItemStatus.LOST else ItemStatus.LOST
            
            # Get candidate items
            candidates = self.db.query(Item).filter(
                and_(
                    Item.status == opposite_status,
                    Item.is_active == True,
                    Item.id != item_id
                )
            ).all()
            
            matches = []
            
            for candidate in candidates:
                # Skip if match already exists
                existing_match = self.db.query(Match).filter(
                    and_(
                        Match.item_id == item_id,
                        Match.matched_item_id == candidate.id
                    )
                ).first()
                
                if existing_match and not force_refresh:
                    continue
                
                # Calculate distance
                distance = self.calculate_distance(
                    item.latitude, item.longitude,
                    candidate.latitude, candidate.longitude
                )
                
                # Skip if too far
                if distance > self.max_distance_km:
                    continue
                
                # Calculate text similarity
                item_text = f"{item.title} {item.description} {item.brand or ''} {item.model or ''} {item.color or ''}"
                candidate_text = f"{candidate.title} {candidate.description} {candidate.brand or ''} {candidate.model or ''} {candidate.color or ''}"
                
                text_similarity = self.calculate_text_similarity(item_text, candidate_text)
                
                # Skip if text similarity too low
                if text_similarity < self.min_similarity_threshold:
                    continue
                
                # Calculate location similarity (inverse of normalized distance)
                location_similarity = max(0, 1 - (distance / self.max_distance_km))
                
                # Calculate base score
                base_score = (text_similarity * self.text_weight) + (location_similarity * self.location_weight)
                
                # Calculate bonuses
                category_bonus = self.calculate_category_bonus(item.category, candidate.category)
                brand_color_bonus, brand_match, color_match = self.calculate_brand_color_bonus(item, candidate)
                time_bonus = self.calculate_time_decay(item.date_lost_found, candidate.date_lost_found)
                
                # Final score with bonuses
                final_score = min(1.0, base_score + category_bonus + brand_color_bonus + time_bonus)
                
                # Determine confidence level
                if final_score >= 0.8:
                    confidence = "high"
                elif final_score >= 0.6:
                    confidence = "medium"
                else:
                    confidence = "low"
                
                # Generate match reason
                match_reason = self._generate_match_reason(
                    text_similarity, distance, item.category == candidate.category,
                    brand_match, color_match
                )
                
                # Create match record
                match = Match(
                    item_id=item.id,
                    matched_item_id=candidate.id,
                    similarity_score=final_score,
                    text_similarity=text_similarity,
                    location_similarity=location_similarity,
                    distance_km=distance,
                    category_match=(item.category == candidate.category),
                    brand_match=brand_match,
                    color_match=color_match,
                    confidence_level=confidence,
                    match_reason=match_reason
                )
                
                self.db.add(match)
                
                matches.append({
                    "match": match,
                    "item": candidate,
                    "score": final_score,
                    "distance": distance,
                    "confidence": confidence,
                    "text_similarity": text_similarity,
                    "location_similarity": location_similarity
                })
            
            # Commit matches to database
            self.db.commit()
            
            # Update item match count
            item.match_count = len(matches)
            self.db.commit()
            
            # Sort by score and return top 10
            matches.sort(key=lambda x: x["score"], reverse=True)
            top_matches = matches[:10]
            
            # Create notifications for high-confidence matches
            self._create_match_notifications(item, top_matches)
            
            logger.info(f"Found {len(top_matches)} matches for item {item_id}")
            return top_matches
            
        except Exception as e:
            logger.error(f"Error finding matches for item {item_id}: {e}")
            self.db.rollback()
            return []
    
    def _generate_match_reason(self, text_sim: float, distance: float, 
                             category_match: bool, brand_match: bool, color_match: bool) -> str:
        """Generate human-readable match reason"""
        reasons = []
        
        if text_sim >= 0.8:
            reasons.append("Very similar description")
        elif text_sim >= 0.6:
            reasons.append("Similar description")
        
        if distance <= 5:
            reasons.append("Very close location")
        elif distance <= 20:
            reasons.append("Nearby location")
        
        if category_match:
            reasons.append("Same category")
        
        if brand_match:
            reasons.append("Same brand")
        
        if color_match:
            reasons.append("Same color")
        
        return ", ".join(reasons) if reasons else "Basic similarity match"
    
    def _create_match_notifications(self, item: Item, matches: List[Dict]):
        """Create notifications for high-confidence matches"""
        try:
            high_confidence_matches = [m for m in matches if m["confidence"] == "high"]
            
            if high_confidence_matches:
                # Notify item owner
                notification = Notification(
                    user_id=item.user_id,
                    title="🎉 High Confidence Match Found!",
                    message=f"We found {len(high_confidence_matches)} high-confidence match(es) for your {item.status} item '{item.title}'",
                    type="match",
                    item_id=item.id
                )
                self.db.add(notification)
                
                # Notify owners of matched items
                for match_data in high_confidence_matches[:3]:  # Limit to top 3
                    matched_item = match_data["item"]
                    notification = Notification(
                        user_id=matched_item.user_id,
                        title="🔍 Potential Match Found!",
                        message=f"Your {matched_item.status} item '{matched_item.title}' might match a {item.status} item",
                        type="match",
                        item_id=matched_item.id,
                        related_user_id=item.user_id
                    )
                    self.db.add(notification)
                
                self.db.commit()
                
        except Exception as e:
            logger.error(f"Error creating match notifications: {e}")
    
    def get_matches_for_item(self, item_id: int, limit: int = 10) -> List[Match]:
        """Get existing matches for an item"""
        return (self.db.query(Match)
                .filter(Match.item_id == item_id)
                .order_by(Match.similarity_score.desc())
                .limit(limit)
                .all())
    
    def confirm_match(self, match_id: int, user_id: int) -> bool:
        """Confirm a match (mark as confirmed)"""
        try:
            match = self.db.query(Match).filter(Match.id == match_id).first()
            if not match:
                return False
            
            # Verify user owns one of the items
            item = self.db.query(Item).filter(Item.id == match.item_id).first()
            matched_item = self.db.query(Item).filter(Item.id == match.matched_item_id).first()
            
            if not (item.user_id == user_id or matched_item.user_id == user_id):
                return False
            
            match.is_confirmed = True
            
            # Update item statuses
            item.status = ItemStatus.MATCHED
            matched_item.status = ItemStatus.MATCHED
            
            self.db.commit()
            
            # Create notifications
            self._create_confirmation_notifications(match, item, matched_item, user_id)
            
            return True
            
        except Exception as e:
            logger.error(f"Error confirming match {match_id}: {e}")
            self.db.rollback()
            return False
    
    def dismiss_match(self, match_id: int, user_id: int) -> bool:
        """Dismiss a match (mark as not relevant)"""
        try:
            match = self.db.query(Match).filter(Match.id == match_id).first()
            if not match:
                return False
            
            # Verify user owns one of the items
            item = self.db.query(Item).filter(Item.id == match.item_id).first()
            matched_item = self.db.query(Item).filter(Item.id == match.matched_item_id).first()
            
            if not (item.user_id == user_id or matched_item.user_id == user_id):
                return False
            
            match.is_dismissed = True
            self.db.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"Error dismissing match {match_id}: {e}")
            self.db.rollback()
            return False
    
    def _create_confirmation_notifications(self, match: Match, item: Item, matched_item: Item, confirming_user_id: int):
        """Create notifications when a match is confirmed"""
        try:
            # Notify the other user
            other_user_id = matched_item.user_id if item.user_id == confirming_user_id else item.user_id
            
            notification = Notification(
                user_id=other_user_id,
                title="✅ Match Confirmed!",
                message=f"A match has been confirmed for items '{item.title}' and '{matched_item.title}'",
                type="match",
                item_id=item.id,
                related_user_id=confirming_user_id
            )
            self.db.add(notification)
            self.db.commit()
            
        except Exception as e:
            logger.error(f"Error creating confirmation notifications: {e}")
    
    def bulk_rematch_items(self, status: Optional[ItemStatus] = None, limit: int = 100):
        """Bulk rematch items (useful for improving algorithm)"""
        try:
            query = self.db.query(Item).filter(Item.is_active == True)
            
            if status:
                query = query.filter(Item.status == status)
            
            items = query.limit(limit).all()
            
            for item in items:
                self.find_matches(item.id, force_refresh=True)
            
            logger.info(f"Bulk rematched {len(items)} items")
            
        except Exception as e:
            logger.error(f"Error in bulk rematch: {e}")
    
    def get_matching_statistics(self) -> Dict:
        """Get statistics about matching performance"""
        try:
            total_items = self.db.query(Item).filter(Item.is_active == True).count()
            total_matches = self.db.query(Match).count()
            confirmed_matches = self.db.query(Match).filter(Match.is_confirmed == True).count()
            high_confidence_matches = self.db.query(Match).filter(Match.confidence_level == "high").count()
            
            avg_similarity = self.db.query(func.avg(Match.similarity_score)).scalar() or 0
            avg_distance = self.db.query(func.avg(Match.distance_km)).scalar() or 0
            
            return {
                "total_items": total_items,
                "total_matches": total_matches,
                "confirmed_matches": confirmed_matches,
                "high_confidence_matches": high_confidence_matches,
                "confirmation_rate": confirmed_matches / total_matches if total_matches > 0 else 0,
                "average_similarity_score": round(avg_similarity, 3),
                "average_distance_km": round(avg_distance, 2)
            }
            
        except Exception as e:
            logger.error(f"Error getting matching statistics: {e}")
            return {}