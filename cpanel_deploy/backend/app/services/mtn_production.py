"""
MTN Mobile Money Production Service for Rwanda
Real payment integration with proper error handling
"""
import requests
import uuid
import base64
import logging
from typing import Dict, Optional
from datetime import datetime, timedelta
from ..core.config import settings

logger = logging.getLogger(__name__)

class MTNMoMoProduction:
    """Production-ready MTN Mobile Money service for Rwanda"""
    
    def __init__(self):
        self.base_url = settings.MTN_MOMO_BASE_URL
        self.subscription_key = settings.MTN_MOMO_SUBSCRIPTION_KEY
        self.api_user = settings.MTN_MOMO_API_USER
        self.api_key = settings.MTN_MOMO_API_KEY
        self.target_environment = settings.MTN_MOMO_TARGET_ENVIRONMENT
        self.callback_url = settings.MTN_MOMO_CALLBACK_URL
        self._token_cache = None
        self._token_expiry = None
    
    def is_configured(self) -> bool:
        """Check if MTN MoMo is configured"""
        return all([
            settings.MTN_MOMO_ENABLED,
            self.subscription_key,
            self.api_user,
            self.api_key
        ])
    
    def _get_basic_auth(self) -> str:
        """Generate Basic Auth header"""
        credentials = f"{self.api_user}:{self.api_key}"
        return base64.b64encode(credentials.encode()).decode()
    
    def get_access_token(self) -> Optional[str]:
        """Get OAuth token with caching"""
        try:
            # Return cached token if valid
            if self._token_cache and self._token_expiry and datetime.now() < self._token_expiry:
                return self._token_cache
            
            url = f"{self.base_url}/collection/token/"
            headers = {
                "Ocp-Apim-Subscription-Key": self.subscription_key,
                "Authorization": f"Basic {self._get_basic_auth()}"
            }
            
            response = requests.post(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                self._token_cache = data.get("access_token")
                # Cache for 50 minutes (tokens usually valid for 1 hour)
                self._token_expiry = datetime.now() + timedelta(minutes=50)
                logger.info("MTN access token obtained successfully")
                return self._token_cache
            else:
                logger.error(f"MTN token error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting MTN token: {e}")
            return None
    
    def request_payment(
        self,
        phone_number: str,
        amount: float,
        external_id: str,
        description: str = "IMIS Contact Unlock"
    ) -> Dict:
        """
        Request payment from customer
        
        Args:
            phone_number: Customer phone (250788123456)
            amount: Amount in RWF
            external_id: Your transaction reference
            description: Payment description
        """
        try:
            if not self.is_configured():
                return {
                    "success": False,
                    "message": "MTN MoMo not configured"
                }
            
            # Get access token
            token = self.get_access_token()
            if not token:
                return {
                    "success": False,
                    "message": "Failed to authenticate with MTN"
                }
            
            # Generate reference ID
            reference_id = str(uuid.uuid4())
            
            # Clean phone number
            clean_phone = phone_number.replace(" ", "").replace("-", "").replace("+", "")
            if not clean_phone.startswith("250"):
                clean_phone = "250" + clean_phone.lstrip("0")
            
            # Prepare request - Try both endpoints
            url = f"{self.base_url}/collection/v1_0/requesttopay"
            headers = {
                "X-Reference-Id": reference_id,
                "X-Target-Environment": self.target_environment,
                "Ocp-Apim-Subscription-Key": self.subscription_key,
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "amount": str(int(amount)),
                "currency": "RWF",
                "externalId": external_id,
                "payer": {
                    "partyIdType": "MSISDN",
                    "partyId": clean_phone
                },
                "payerMessage": description,
                "payeeNote": f"IMIS Payment - {external_id}"
            }
            
            # Don't include callback URL if not publicly accessible
            # if self.callback_url:
            #     payload["callbackUrl"] = self.callback_url
            
            logger.info(f"Requesting MTN payment: {amount} RWF from {clean_phone}")
            
            # Make request
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 202:
                logger.info(f"MTN payment request successful: {reference_id}")
                return {
                    "success": True,
                    "reference_id": reference_id,
                    "message": f"Payment request sent to {clean_phone}. Please check your phone and enter your PIN.",
                    "phone": clean_phone
                }
            else:
                error_msg = response.text
                logger.error(f"MTN payment failed: {response.status_code} - {error_msg}")
                return {
                    "success": False,
                    "message": f"Payment request failed. Please try again or contact support.",
                    "error": error_msg
                }
                
        except requests.Timeout:
            logger.error("MTN API timeout")
            return {
                "success": False,
                "message": "Request timeout. Please try again."
            }
        except Exception as e:
            logger.error(f"MTN payment error: {e}")
            return {
                "success": False,
                "message": "Payment request failed. Please try again."
            }
    
    def check_status(self, reference_id: str) -> Dict:
        """
        Check payment status
        
        Args:
            reference_id: The X-Reference-Id from request_payment
        """
        try:
            if not self.is_configured():
                return {"success": False, "message": "MTN MoMo not configured"}
            
            token = self.get_access_token()
            if not token:
                return {"success": False, "message": "Authentication failed"}
            
            url = f"{self.base_url}/collection/v1_0/requesttopay/{reference_id}"
            headers = {
                "X-Target-Environment": self.target_environment,
                "Ocp-Apim-Subscription-Key": self.subscription_key,
                "Authorization": f"Bearer {token}"
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                status = data.get("status", "").upper()
                
                logger.info(f"MTN payment status for {reference_id}: {status}")
                
                return {
                    "success": True,
                    "status": status,
                    "amount": data.get("amount"),
                    "currency": data.get("currency"),
                    "financial_transaction_id": data.get("financialTransactionId"),
                    "reason": data.get("reason")
                }
            else:
                logger.error(f"MTN status check failed: {response.status_code}")
                return {
                    "success": False,
                    "message": "Failed to check payment status"
                }
                
        except Exception as e:
            logger.error(f"Error checking MTN status: {e}")
            return {
                "success": False,
                "message": "Status check failed"
            }
    
    def get_balance(self) -> Dict:
        """Get account balance (for monitoring)"""
        try:
            if not self.is_configured():
                return {"success": False, "message": "Not configured"}
            
            token = self.get_access_token()
            if not token:
                return {"success": False, "message": "Authentication failed"}
            
            url = f"{self.base_url}/collection/v1_0/account/balance"
            headers = {
                "X-Target-Environment": self.target_environment,
                "Ocp-Apim-Subscription-Key": self.subscription_key,
                "Authorization": f"Bearer {token}"
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "balance": data.get("availableBalance"),
                    "currency": data.get("currency")
                }
            else:
                return {"success": False, "message": "Failed to get balance"}
                
        except Exception as e:
            logger.error(f"Error getting balance: {e}")
            return {"success": False, "message": "Balance check failed"}

# Singleton instance
mtn_service = MTNMoMoProduction()
