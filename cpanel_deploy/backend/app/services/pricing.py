"""Dynamic pricing service for different item categories"""

from typing import Dict, Tuple

class PricingService:
    """Service to calculate prices and commissions based on item category"""
    
    # Base prices in RWF for different categories
    CATEGORY_PRICES = {
        "phone": 2000,           # High value electronics
        "electronics": 1800,     # Laptops, tablets, etc.
        "documents": 1500,       # ID cards, passports, certificates
        "wallet": 1200,          # Wallets with potential money/cards
        "jewelry": 1000,         # Rings, necklaces, watches
        "bag": 800,              # Bags, backpacks
        "keys": 500,             # Car keys, house keys
        "other": 600             # Default for other items
    }
    
    # Commission rates (system takes this percentage)
    SYSTEM_COMMISSION_RATE = 0.15  # 15% to system
    FINDER_RATE = 0.85             # 85% to finder
    
    @classmethod
    def get_unlock_price(cls, category: str) -> int:
        """Get unlock price for a specific category"""
        return cls.CATEGORY_PRICES.get(category.lower(), cls.CATEGORY_PRICES["other"])
    
    @classmethod
    def calculate_commission(cls, unlock_price: int) -> Tuple[int, int]:
        """Calculate commission split between system and finder
        
        Returns:
            Tuple[int, int]: (system_commission, finder_amount)
        """
        system_commission = int(unlock_price * cls.SYSTEM_COMMISSION_RATE)
        finder_amount = unlock_price - system_commission
        
        return system_commission, finder_amount
    
    @classmethod
    def get_pricing_info(cls, category: str) -> Dict:
        """Get complete pricing information for a category"""
        unlock_price = cls.get_unlock_price(category)
        system_commission, finder_amount = cls.calculate_commission(unlock_price)
        
        return {
            "category": category,
            "unlock_price": unlock_price,
            "system_commission": system_commission,
            "finder_amount": finder_amount,
            "commission_rate": cls.SYSTEM_COMMISSION_RATE * 100,
            "currency": "RWF"
        }
    
    @classmethod
    def get_all_category_prices(cls) -> Dict:
        """Get pricing for all categories"""
        return {
            category: cls.get_pricing_info(category) 
            for category in cls.CATEGORY_PRICES.keys()
        }