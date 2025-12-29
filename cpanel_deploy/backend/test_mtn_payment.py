"""Test MTN payment with real phone number"""
from app.services.mtn_production import mtn_service
import uuid

print("Testing MTN MoMo Payment Request...")
print("=" * 50)

# Test with the phone number
phone = "250796014801"
amount = 1000
external_id = f"TEST_{uuid.uuid4().hex[:8].upper()}"

print(f"Phone: {phone}")
print(f"Amount: {amount} RWF")
print(f"Reference: {external_id}")
print()

# Request payment
result = mtn_service.request_payment(
    phone_number=phone,
    amount=amount,
    external_id=external_id,
    description="IMIS Test Payment"
)

print("Result:")
print(f"Success: {result.get('success')}")
print(f"Message: {result.get('message')}")
if result.get('reference_id'):
    print(f"Reference ID: {result.get('reference_id')}")
if result.get('error'):
    print(f"Error: {result.get('error')}")

print()
print("=" * 50)

# If successful, check status
if result.get('success') and result.get('reference_id'):
    print("\nWaiting 5 seconds before checking status...")
    import time
    time.sleep(5)
    
    print("\nChecking payment status...")
    status = mtn_service.check_status(result['reference_id'])
    print(f"Status: {status.get('status')}")
    print(f"Details: {status}")
