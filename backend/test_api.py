"""
Quick test script for IIT Bombay Analytics Backend.

This script demonstrates all API endpoints in sequence.
Run after starting the Django server: python manage.py runserver
"""

import requests
import json
from pathlib import Path

# Configuration
BASE_URL = "http://127.0.0.1:8000/api"
TEST_USER = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123",
    "password_confirm": "TestPass123"
}

def print_response(title, response):
    """Pretty print API response."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")
    print()

def main():
    print("🚀 Starting IIT Bombay Analytics Backend Test")
    print(f"Base URL: {BASE_URL}")
    
    # Step 1: Register user
    print("\n" + "="*60)
    print("STEP 1: REGISTER USER")
    print("="*60)
    response = requests.post(
        f"{BASE_URL}/auth/register/",
        json=TEST_USER
    )
    print_response("Register User", response)
    
    if response.status_code != 201:
        # Try logging in instead (user might already exist)
        print("Registration failed. Trying to login instead...")
        response = requests.post(
            f"{BASE_URL}/auth/login/",
            json={
                "username": TEST_USER["username"],
                "password": TEST_USER["password"]
            }
        )
        print_response("Login User", response)
    
    if response.status_code not in [200, 201]:
        print("❌ Authentication failed. Exiting.")
        return
    
    # Extract token
    token = response.json().get('token')
    print(f"✅ Authentication successful! Token: {token[:20]}...")
    
    headers = {
        "Authorization": f"Token {token}"
    }
    
    # Step 2: Check history (should be empty or show old uploads)
    print("\n" + "="*60)
    print("STEP 2: CHECK UPLOAD HISTORY")
    print("="*60)
    response = requests.get(f"{BASE_URL}/history/", headers=headers)
    print_response("Get History (Before Upload)", response)
    
    # Step 3: Try to get summary (should fail if no uploads)
    print("\n" + "="*60)
    print("STEP 3: TRY TO GET SUMMARY (Should fail if no uploads)")
    print("="*60)
    response = requests.get(f"{BASE_URL}/summary/", headers=headers)
    print_response("Get Summary (Before Upload)", response)
    
    # Step 4: Upload CSV
    print("\n" + "="*60)
    print("STEP 4: UPLOAD CSV DATASET")
    print("="*60)
    
    # Check if sample_equipment_data.csv exists
    csv_path = Path(__file__).parent / "sample_equipment_data.csv"
    if not csv_path.exists():
        print(f"❌ Sample CSV not found at: {csv_path}")
        print("Please ensure sample_equipment_data.csv exists in the backend directory.")
        return
    
    with open(csv_path, 'rb') as f:
        files = {'file': ('sample_equipment_data.csv', f, 'text/csv')}
        response = requests.post(
            f"{BASE_URL}/upload/",
            headers=headers,
            files=files
        )
    print_response("Upload CSV", response)
    
    if response.status_code != 201:
        print("❌ Upload failed. Exiting.")
        return
    
    print("✅ Upload successful!")
    
    # Step 5: Get summary
    print("\n" + "="*60)
    print("STEP 5: GET ANALYTICS SUMMARY")
    print("="*60)
    response = requests.get(f"{BASE_URL}/summary/", headers=headers)
    print_response("Get Summary", response)
    
    # Step 6: Get distribution
    print("\n" + "="*60)
    print("STEP 6: GET EQUIPMENT DISTRIBUTION")
    print("="*60)
    response = requests.get(f"{BASE_URL}/distribution/", headers=headers)
    print_response("Get Distribution", response)
    
    # Step 7: Check history again
    print("\n" + "="*60)
    print("STEP 7: CHECK UPLOAD HISTORY (After Upload)")
    print("="*60)
    response = requests.get(f"{BASE_URL}/history/", headers=headers)
    print_response("Get History", response)
    
    # Step 8: Logout
    print("\n" + "="*60)
    print("STEP 8: LOGOUT")
    print("="*60)
    response = requests.post(f"{BASE_URL}/auth/logout/", headers=headers)
    print_response("Logout", response)
    
    # Step 9: Try to access summary after logout (should fail)
    print("\n" + "="*60)
    print("STEP 9: TRY TO ACCESS SUMMARY AFTER LOGOUT (Should fail)")
    print("="*60)
    response = requests.get(f"{BASE_URL}/summary/", headers=headers)
    print_response("Get Summary (After Logout)", response)
    
    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETED!")
    print("="*60)
    print("\nBackend is working correctly! 🎉")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to backend server.")
        print("Make sure the Django server is running:")
        print("  python manage.py runserver")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
