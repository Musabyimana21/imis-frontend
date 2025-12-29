"""Alternative payment methods for IMIS"""

import uuid
from typing import Dict
from datetime import datetime

class PaymentAlternatives:
    """Handle alternative payment methods when MTN is unavailable"""
    
    def __init__(self):
        self.methods = {
            "airtel_money": {
                "name": "Airtel Money",
                "code": "*182*7*1#",
                "phone": "+250788123456",
                "instructions": "Dial *182*7*1# and follow prompts"
            },
            "bank_transfer": {
                "name": "Bank of Kigali",
                "account": "123456789",
                "swift": "BKRWRWRW",
                "instructions": "Transfer to account 123456789 (IMIS Rwanda)"
            },
            "tigo_cash": {
                "name": "Tigo Cash",
                "code": "*144#",
                "instructions": "Dial *144# for Tigo Cash payments"
            }
        }
    
    def generate_payment_reference(self) -> str:
        """Generate unique payment reference"""
        return f"IMIS-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
    
    def get_payment_instructions(self, amount: int, method: str = "all") -> Dict:
        """Get payment instructions for alternative methods"""
        reference = self.generate_payment_reference()
        
        if method != "all" and method in self.methods:
            return {
                "reference": reference,
                "amount": amount,
                "method": self.methods[method],
                "instructions": f"Pay {amount} RWF using {self.methods[method]['name']}. Reference: {reference}"
            }
        
        return {
            "reference": reference,
            "amount": amount,
            "methods": self.methods,
            "instructions": f"Pay {amount} RWF using any method below. Reference: {reference}",
            "support_phone": "+250780460621",
            "support_email": "gaudencemusabyimana21@gmail.com"
        }
    
    def verify_manual_payment(self, reference: str, method: str, phone: str) -> Dict:
        """Simulate manual payment verification"""
        return {
            "success": True,
            "reference": reference,
            "method": method,
            "phone": phone,
            "status": "pending_verification",
            "message": "Payment received. Verification in progress.",
            "estimated_verification": "2-5 minutes"
        }