"""MTN Mobile Money API integration service"""

import requests
import uuid
import json
from typing import Dict, Optional
import importlib
from ..core import config
importlib.reload(config)
from ..core.config import settings

class MTNMoMoService:
    """MTN Mobile Money API integration"""
    
    def __init__(self):
        self.base_url = settings.MTN_MOMO_BASE_URL
        self.subscription_key = settings.MTN_MOMO_SUBSCRIPTION_KEY
        self.api_user = settings.MTN_MOMO_API_USER
        self.api_key = settings.MTN_MOMO_API_KEY
        self.callback_url = settings.MTN_MOMO_CALLBACK_URL
        self.callback_host = settings.MTN_MOMO_CALLBACK_HOST
        self.target_environment = settings.MTN_MOMO_TARGET_ENVIRONMENT
        self.account = settings.MTN_MOMO_ACCOUNT
        
    def get_access_token(self) -> Optional[str]:
        """Get access token for API calls"""
        if not all([self.subscription_key, self.api_user, self.api_key]):
            print("Missing MTN credentials")
            return None
            
        url = f"{self.base_url}/collection/token/"
        
        # Create basic auth from api_user:api_key
        import base64
        credentials = f"{self.api_user}:{self.api_key}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Ocp-Apim-Subscription-Key": self.subscription_key,
            "X-Target-Environment": self.target_environment
        }
        
        print(f"Requesting token from: {url}")
        print(f"Headers: {headers}")
        
        try:
            response = requests.post(url, headers=headers)
            print(f"Token response status: {response.status_code}")
            print(f"Token response: {response.text}")
            
            if response.status_code == 200:
                return response.json().get("access_token")
            else:
                print(f"Token request failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error getting access token: {e}")
        
        return None
    
    def request_to_pay(self, phone: str, amount: int, reference_id: str = None) -> Dict:
        """Request payment from user
        
        Args:
            phone: Phone number in format 25078XXXXXXX
            amount: Amount in RWF
            reference_id: Optional reference ID
            
        Returns:
            Dict with transaction details
        """
        if not settings.MTN_MOMO_ENABLED:
            return self._simulate_payment(phone, amount, reference_id)
        
        access_token = self.get_access_token()
        if not access_token:
            return {"success": False, "error": "Failed to get access token"}
        
        if not reference_id:
            reference_id = str(uuid.uuid4())
        
        url = f"{self.base_url}/collection/v1_0/requesttopay"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Reference-Id": reference_id,
            "X-Target-Environment": self.target_environment,
            "Ocp-Apim-Subscription-Key": self.subscription_key,
            "Content-Type": "application/json"
        }
        
        # Format phone number for Rwanda (0788123456 -> 250788123456)
        phone = phone.replace("+", "").replace(" ", "").replace("-", "")
        
        if phone.startswith("250"):
            phone = phone  # Already correct: 250788123456
        elif phone.startswith("0") and len(phone) == 10:
            phone = "250" + phone[1:]  # 0788123456 -> 250788123456
        elif len(phone) == 9:
            phone = "250" + phone  # 788123456 -> 250788123456
        else:
            phone = "250" + phone.lstrip("0")  # Remove any leading zeros
            
        print(f"Formatted phone: {phone}")
        
        payload = {
            "amount": str(amount),
            "currency": "RWF",
            "externalId": reference_id,
            "payer": {
                "partyIdType": "MSISDN",
                "partyId": phone
            },
            "payerMessage": "Payment for IMIS item unlock",
            "payeeNote": f"IMIS unlock fee - {amount} RWF"
        }
        
        print(f"Payment request URL: {url}")
        print(f"Payment payload: {json.dumps(payload, indent=2)}")
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            
            print(f"Payment response status: {response.status_code}")
            print(f"Payment response headers: {dict(response.headers)}")
            print(f"Payment response body: '{response.text}'")
            
            if response.status_code == 202:
                return {
                    "success": True,
                    "reference_id": reference_id,
                    "status": "PENDING",
                    "message": f"Payment request sent to {phone}. Please check your phone and enter PIN."
                }
            else:
                return {
                    "success": False,
                    "error": f"Payment failed: Status {response.status_code} - Headers: {dict(response.headers)} - Body: {response.text}"
                }
                
        except Exception as e:
            print(f"Payment exception: {e}")
            from .payment_alternatives import PaymentAlternatives
            alt_payments = PaymentAlternatives()
            payment_info = alt_payments.get_payment_instructions(amount)
            
            return {
                "success": False,
                "error": "MTN Mobile Money temporarily unavailable",
                "payment_reference": payment_info["reference"],
                "alternatives": {
                    "airtel_money": {
                        "name": "Airtel Money",
                        "code": "*182*7*1#",
                        "instructions": f"Dial *182*7*1# → Send Money → {payment_info['reference']}"
                    },
                    "bank_transfer": {
                        "name": "Bank of Kigali",
                        "account": "123456789",
                        "instructions": f"Transfer {amount} RWF to 123456789. Reference: {payment_info['reference']}"
                    },
                    "tigo_cash": {
                        "name": "Tigo Cash",
                        "code": "*144#",
                        "instructions": f"Dial *144# → Send Money → Reference: {payment_info['reference']}"
                    },
                    "manual_verification": {
                        "whatsapp": "+250780460621",
                        "instructions": f"Send payment screenshot to WhatsApp +250780460621 with reference: {payment_info['reference']}"
                    }
                },
                "support_contact": "+250780460621",
                "verification_time": "2-5 minutes after payment",
                "technical_error": str(e)
            }
    
    def check_payment_status(self, reference_id: str) -> Dict:
        """Check payment status"""
        if not settings.MTN_MOMO_ENABLED:
            return {"status": "SUCCESSFUL", "reason": "Simulated payment completed"}
        
        access_token = self.get_access_token()
        if not access_token:
            return {"status": "FAILED", "reason": "Failed to get access token"}
        
        url = f"{self.base_url}/collection/v1_0/requesttopay/{reference_id}"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Target-Environment": self.target_environment,
            "Ocp-Apim-Subscription-Key": self.subscription_key
        }
        
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": data.get("status", "PENDING"),
                    "reason": data.get("reason", ""),
                    "amount": data.get("amount"),
                    "currency": data.get("currency")
                }
            else:
                return {"status": "FAILED", "reason": f"Status check failed: {response.text}"}
                
        except Exception as e:
            return {"status": "FAILED", "reason": f"Status check error: {str(e)}"}
    
    def _simulate_payment(self, phone: str, amount: int, reference_id: str = None) -> Dict:
        """Simulate payment for testing"""
        if not reference_id:
            reference_id = str(uuid.uuid4())
        
        print(f"SIMULATION: Payment of {amount} RWF from {phone}")
        return {
            "success": True,
            "reference_id": reference_id,
            "status": "SUCCESSFUL",
            "message": f"SIMULATION: Payment of {amount} RWF completed successfully. Contact unlocked!"
        }