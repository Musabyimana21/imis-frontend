"""
Simple matching system without scikit-learn dependency
Uses built-in Python libraries for text similarity
"""

from difflib import SequenceMatcher
from typing import List, Dict, Any
import re
from geopy.distance import geodesic


def clean_text(text: str) -> str:
    """Clean and normalize text for comparison"""
    if not text:
        return ""
    # Convert to lowercase and remove extra spaces
    text = re.sub(r'\s+', ' ', text.lower().strip())
    # Remove special characters but keep letters, numbers, and spaces
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text


def calculate_text_similarity(text1: str, text2: str) -> float:
    """Calculate text similarity using SequenceMatcher"""
    clean1 = clean_text(text1)
    clean2 = clean_text(text2)
    
    if not clean1 or not clean2:
        return 0.0
    
    # Use SequenceMatcher for similarity
    similarity = SequenceMatcher(None, clean1, clean2).ratio()
    
    # Boost similarity for exact word matches
    words1 = set(clean1.split())
    words2 = set(clean2.split())
    
    if words1 and words2:
        word_overlap = len(words1.intersection(words2)) / len(words1.union(words2))
        # Combine sequence similarity with word overlap
        similarity = (similarity * 0.7) + (word_overlap * 0.3)
    
    return min(similarity, 1.0)


def calculate_location_similarity(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate location similarity based on distance"""
    if not all([lat1, lon1, lat2, lon2]):
        return 0.0
    
    try:
        # Calculate distance in kilometers
        distance = geodesic((lat1, lon1), (lat2, lon2)).kilometers
        
        # Convert distance to similarity score (closer = higher score)
        if distance <= 1:  # Within 1km
            return 1.0
        elif distance <= 5:  # Within 5km
            return 0.8
        elif distance <= 10:  # Within 10km
            return 0.6
        elif distance <= 20:  # Within 20km
            return 0.4
        elif distance <= 50:  # Within 50km
            return 0.2
        else:
            return 0.1
    except Exception:
        return 0.0


def calculate_category_similarity(cat1: str, cat2: str) -> float:
    """Calculate category similarity"""
    if not cat1 or not cat2:
        return 0.0
    
    cat1_clean = clean_text(cat1)
    cat2_clean = clean_text(cat2)
    
    if cat1_clean == cat2_clean:
        return 1.0
    
    # Check for partial matches
    return calculate_text_similarity(cat1_clean, cat2_clean)


def find_matches(lost_items: List[Any], found_items: List[Any], threshold: float = 0.3) -> List[Dict]:
    """
    Find matches between lost and found items
    
    Args:
        lost_items: List of lost item objects
        found_items: List of found item objects  
        threshold: Minimum similarity threshold (0.0 to 1.0)
    
    Returns:
        List of match dictionaries sorted by similarity score
    """
    matches = []
    
    for lost in lost_items:
        for found in found_items:
            # Calculate text similarity (70% weight)
            text_sim = calculate_text_similarity(
                f"{lost.title} {lost.description}",
                f"{found.title} {found.description}"
            )
            
            # Calculate location similarity (20% weight)
            location_sim = calculate_location_similarity(
                getattr(lost, 'latitude', None),
                getattr(lost, 'longitude', None),
                getattr(found, 'latitude', None),
                getattr(found, 'longitude', None)
            )
            
            # Calculate category similarity (10% weight)
            category_sim = calculate_category_similarity(
                getattr(lost, 'category', ''),
                getattr(found, 'category', '')
            )
            
            # Combined similarity score
            total_similarity = (
                text_sim * 0.7 +
                location_sim * 0.2 +
                category_sim * 0.1
            )
            
            # Only include matches above threshold
            if total_similarity >= threshold:
                matches.append({
                    'lost_item': lost,
                    'found_item': found,
                    'similarity': total_similarity,
                    'text_similarity': text_sim,
                    'location_similarity': location_sim,
                    'category_similarity': category_sim,
                    'match_score': int(total_similarity * 100)  # Percentage
                })
    
    # Sort by similarity score (highest first)
    matches.sort(key=lambda x: x['similarity'], reverse=True)
    
    return matches


def get_top_matches(lost_items: List[Any], found_items: List[Any], limit: int = 10) -> List[Dict]:
    """Get top N matches"""
    all_matches = find_matches(lost_items, found_items)
    return all_matches[:limit]


def match_single_item(target_item: Any, candidate_items: List[Any], limit: int = 5) -> List[Dict]:
    """Find matches for a single item against a list of candidates"""
    if target_item.item_type == 'lost':
        matches = find_matches([target_item], candidate_items)
    else:
        matches = find_matches(candidate_items, [target_item])
    
    return matches[:limit]


# Compatibility function for existing code
def calculate_similarity(text1: str, text2: str) -> float:
    """Backward compatibility function"""
    return calculate_text_similarity(text1, text2)