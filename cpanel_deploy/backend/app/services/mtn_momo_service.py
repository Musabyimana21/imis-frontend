import requests
import uuid
import json
import logging
from typing import Dict, Optional
from datetime import datetime
from ..core.config import settings

logger = logging.getLogger(__name__)

class MTNMoMoService:
    """
    MTN Mobile Money API Integration Service
    Documentation: https://momodeveloper.mtn.com/
    """
    
    def __init__(self):
        self.enabled = settings.MTN_MOMO_ENABLED
        self.base_url = settings.MTN_MOMO_BASE_URL
        self.subscription_key = settings.MTN_MOMO_SUBSCRIPTION_KEY
        self.api_user = settings.MTN_MOMO_API_USER
        self.api_key = settings.MTN_MOMO_API_KEY
        self.target_environment = settings.MTN_MOMO_TARGET_ENVIRONMENT
        self.callback_url = settings.MTN_MOMO_CALLBACK_URL
        
    def is_configured(self) -> bool:
        """Check if MTN MoMo is properly configured"""
        return (
            self.enabled and
            self.subscription_key is not None and
            self.api_user is not None and
            self.api_key is not None
        )
    
    def get_access_token(self) -> Optional[str]:
        """Get OAuth access token from MTN MoMo API"""
        try:
            url = f"{self.base_url}/collection/token/"
            headers = {
                "Ocp-Apim-Subscription-Key": self.subscription_key,
                "Authorization": f"Basic {self._get_basic_auth()}"
            }
            
            response = requests.post(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("access_token")
            else:
                logger.error(f"Failed to get MTN access token: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting MTN access token: {e}")
            return None
    
    def _get_basic_auth(self) -> str:
        """Generate Basic Auth string"""
        import base64
        credentials = f"{self.api_user}:{self.api_key}"
        return base64.b64encode(credentials.encode()).decode()
    
    def request_to_pay(
        self,
        amount: float,
        phone_number: str,
        external_id: str,
        payer_message: str = "Payment for IMIS",
        payee_note: str = "Contact unlock fee"
    ) -> Dict:
        """
        Request payment from customer
        
        Args:
            amount: Amount in RWF
            phone_number: Customer phone number (format: 250788123456)
            external_id: Your transaction reference
            payer_message: Message shown to payer
            payee_note: Internal note
            
        Returns:
            Dict with success status and reference_id
        """
        try:
            if not self.is_configured():
                return {
                    "success": False,
                    "message": "MTN MoMo not configured. Using simulation mode.",
                    "simulation": True
                }
            
            # Get access token
            access_token = self.get_access_token()
            if not access_token:
                return {"success": False, "message": "Failed to authenticate with MTN"}
            
            # Generate unique reference ID
            reference_id = str(uuid.uuid4())
            
            # Prepare request
            url = f"{self.base_url}/collection/v1_0/requesttopay"
            headers = {
                "X-Reference-Id": reference_id,
                "X-Target-Environment": self.target_environment,
                "Ocp-Apim-Subscription-Key": self.subscription_key,
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            # Clean phone number (remove spaces, dashes)
            clean_phone = phone_number.replace(" ", "").replace("-", "")
            if not clean_phone.startswith("250"):
                clean_phone = "250" + clean_phone.lstrip("0")
            
            payload = {
                "amount": str(amount),
                "currency": "RWF",
                "externalId": external_id,
                "payer": {
                    "partyIdType": "MSISDN",
                    "partyId": clean_phone
                },
                "payerMessage": payer_message,
                "payeeNote": payee_note
            }
            
            if self.callback_url:
                payload["callbackUrl"] = self.callback_url
            
            # Make request
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 202:
                logger.info(f"MTN payment request successful: {reference_id}")
                return {
                    "success": True,
                    "reference_id": reference_id,
                    "message": "Payment request sent to customer's phone"
                }
            else:
                logger.error(f"MTN payment request failed: {response.status_code} - {response.text}")
                return {
                    "success": False,
                    "message": f"Payment request failed: {response.text}"
                }
                
        except requests.Timeout:
            logger.error("MTN API request timeout")
            return {"success": False, "message": "Request timeout. Please try again."}
        except Exception as e:
            logger.error(f"Error requesting MTN payment: {e}")
            return {"success": False, "message": "Payment request failed"}
    
    def check_payment_status(self, reference_id: str) -> Dict:
        """
        Check status of a payment request
        
        Args:
            reference_id: The X-Reference-Id from request_to_pay
            
        Returns:
            Dict with status information
        """
        try:
            if not self.is_configured():
                return {"success": False, "message": "MTN MoMo not configured"}
            
            # Get access token
            access_token = self.get_access_token()
            if not access_token:
                return {"success": False, "message": "Failed to authenticate"}
            
            # Check status
            url = f"{self.base_url}/collection/v1_0/requesttopay/{reference_id}"
            headers = {
                "X-Target-Environment": self.target_environment,
                "Ocp-Apim-Subscription-Key": self.subscription_key,
                "Authorization": f"Bearer {access_token}"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                status = data.get("status")
                
                return {
                    "success": True,
                    "status": status,
                    "amount": data.get("amount"),
                    "currency": data.get("currency"),
                    "financial_transaction_id": data.get("financialTransactionId"),
                    "external_id": data.get("externalId"),
                    "reason": data.get("reason")
                }
            else:
                logger.error(f"Failed to check payment status: {response.status_code}")
                return {"success": False, "message": "Failed to check status"}
                
        except Exception as e:
            logger.error(f"Error checking payment status: {e}")
            return {"success": False, "message": "Status check failed"}
    
    def get_account_balance(self) -> Dict:
        """Get account balance (for admin/monitoring)"""
        try:
            if not self.is_configured():
                return {"success": False, "message": "MTN MoMo not configured"}
            
            access_token = self.get_access_token()
            if not access_token:
                return {"success": False, "message": "Failed to authenticate"}
            
            url = f"{self.base_url}/collection/v1_0/account/balance"
            headers = {
                "X-Target-Environment": self.target_environment,
                "Ocp-Apim-Subscription-Key": self.subscription_key,
                "Authorization": f"Bearer {access_token}"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "available_balance": data.get("availableBalance"),
                    "currency": data.get("currency")
                }
            else:
                return {"success": False, "message": "Failed to get balance"}
                
        except Exception as e:
            logger.error(f"Error getting account balance: {e}")
            return {"success": False, "message": "Balance check failed"}

# Singleton instance
mtn_momo_service = MTNMoMoService()
