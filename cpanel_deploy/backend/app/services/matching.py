from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..models.enhanced_models import Item, Match, ItemStatus
import math
from difflib import SequenceMatcher
import re

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

try:
    from geoalchemy2.functions import ST_Distance, ST_GeogFromText
    HAS_POSTGIS = True
except ImportError:
    HAS_POSTGIS = False

class MatchingService:
    def __init__(self, db: Session):
        self.db = db
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text for comparison"""
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text.lower().strip())
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return text
    
    def calculate_text_similarity(self, text1: str, text2: str) -> float:
        if HAS_SKLEARN:
            vectorizer = TfidfVectorizer()
            try:
                tfidf = vectorizer.fit_transform([text1, text2])
                return cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
            except:
                pass
        
        # Fallback to simple similarity
        clean1 = self.clean_text(text1)
        clean2 = self.clean_text(text2)
        
        if not clean1 or not clean2:
            return 0.0
        
        similarity = SequenceMatcher(None, clean1, clean2).ratio()
        
        # Boost for word matches
        words1 = set(clean1.split())
        words2 = set(clean2.split())
        
        if words1 and words2:
            word_overlap = len(words1.intersection(words2)) / len(words1.union(words2))
            similarity = (similarity * 0.7) + (word_overlap * 0.3)
        
        return min(similarity, 1.0)
    
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        if HAS_POSTGIS:
            try:
                point1 = f'POINT({lon1} {lat1})'
                point2 = f'POINT({lon2} {lat2})'
                distance = self.db.query(
                    func.ST_Distance(
                        ST_GeogFromText(point1),
                        ST_GeogFromText(point2)
                    )
                ).scalar()
                return distance / 1000 if distance else 999999
            except:
                pass
        
        # Haversine formula fallback
        R = 6371  # Earth radius in km
        lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
        lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        return R * c
    
    def find_matches(self, item_id: int, max_distance_km: float = 50):
        item = self.db.query(Item).filter(Item.id == item_id).first()
        if not item:
            return []
        
        opposite_status = ItemStatus.FOUND if item.status == ItemStatus.LOST else ItemStatus.LOST
        
        candidates = self.db.query(Item).filter(
            and_(
                Item.status == opposite_status,
                Item.is_active == True,
                Item.id != item_id
            )
        ).all()
        
        matches = []
        for candidate in candidates:
            text_sim = self.calculate_text_similarity(
                f"{item.title} {item.description} {item.category}",
                f"{candidate.title} {candidate.description} {candidate.category}"
            )
            
            distance = self.calculate_distance(
                item.latitude, item.longitude,
                candidate.latitude, candidate.longitude
            )
            
            if distance <= max_distance_km and text_sim > 0.3:
                score = (text_sim * 0.7) + ((1 - min(distance / max_distance_km, 1)) * 0.3)
                
                match = Match(
                    item_id=item.id,
                    matched_item_id=candidate.id,
                    similarity_score=score,
                    distance_km=distance
                )
                self.db.add(match)
                matches.append({
                    "item": candidate,
                    "score": score,
                    "distance": distance
                })
        
        self.db.commit()
        return sorted(matches, key=lambda x: x["score"], reverse=True)[:10]
