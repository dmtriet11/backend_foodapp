"""
🔐 TEST AUTHENTICATION ENDPOINTS
Test login, register, verify functionality
"""

import requests
import json
from datetime import datetime

BASE_URL = "https://backend-foodapp-1-wr4a.onrender.com/api"
# BASE_URL = "http://localhost:5000/api"  # For local testing

def print_test(name, method, endpoint):
    print(f"\n{'='*60}")
    print(f"🧪 Test: {name}")
    print(f"   Method: {method}")
    print(f"   Endpoint: {endpoint}")
    print(f"{'='*60}")

def print_result(success, message, data=None):
    icon = "✅" if success else "❌"
    print(f"{icon} {message}")
    if data:
        if isinstance(data, dict) and len(str(data)) < 500:
            print(f"   Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"   Response: {str(data)[:200]}...")

# ============================================
# TEST 1: REGISTER NEW USER
# ============================================
def test_register():
    print_test("Register New User", "POST", "/register")
    
    # Generate unique email
    timestamp = int(datetime.now().timestamp())
    test_email = f"testuser{timestamp}@example.com"
    
    payload = {
        "email": test_email,
        "password": "Test123456",
        "name": "Test User"  # Field name matches register_route.py requirement
    }
    
    try:
        response = requests.post(f"{BASE_URL}/register", json=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code in [200, 201]:
            data = response.json()
            print_result(True, "Registration successful!", data)
            return True, test_email, "Test123456"
        else:
            data = response.json() if response.content else {}
            print_result(False, f"Registration failed", data)
            return False, None, None
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False, None, None

# ============================================
# TEST 2: LOGIN WITH CREDENTIALS
# ============================================
def test_login(email=None, password=None):
    print_test("Login with Email/Password", "POST", "/login")
    
    # Use provided credentials or test with default
    if not email:
        email = "test@example.com"
        password = "Test123456"
    
    payload = {
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_result(True, "Login successful!", data)
            
            # Extract token if available
            token = data.get('idToken') or data.get('token') or data.get('accessToken')
            if token:
                print(f"   🔑 Token received (first 50 chars): {token[:50]}...")
            
            return True, data
        else:
            data = response.json() if response.content else {}
            print_result(False, "Login failed", data)
            return False, None
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False, None

# ============================================
# TEST 3: VERIFY EMAIL (if verification endpoint exists)
# ============================================
def test_verify(email=None):
    print_test("Verify Email", "POST", "/verify")
    
    if not email:
        email = "test@example.com"
    
    payload = {
        "email": email,
        "code": "123456"  # Test code
    }
    
    try:
        response = requests.post(f"{BASE_URL}/verify", json=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_result(True, "Verification endpoint responding", data)
            return True
        else:
            data = response.json() if response.content else {}
            print_result(False, "Verification failed (expected if code is wrong)", data)
            return False
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

# ============================================
# TEST 4: PROFILE (with authentication)
# ============================================
def test_profile(token=None):
    print_test("Get User Profile", "GET", "/profile")
    
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        response = requests.get(f"{BASE_URL}/profile", headers=headers, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_result(True, "Profile retrieved!", data)
            return True
        elif response.status_code == 401:
            print_result(False, "Unauthorized (token required or invalid)")
            return False
        else:
            data = response.json() if response.content else {}
            print_result(False, "Profile fetch failed", data)
            return False
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

# ============================================
# TEST 5: FORGOT PASSWORD
# ============================================
def test_forgot_password(email=None):
    print_test("Forgot Password", "POST", "/forgot-password")
    
    if not email:
        email = "test@example.com"
    
    payload = {
        "email": email
    }
    
    try:
        response = requests.post(f"{BASE_URL}/forgot-password", json=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_result(True, "Password reset email sent!", data)
            return True
        else:
            data = response.json() if response.content else {}
            print_result(False, "Forgot password failed", data)
            return False
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

# ============================================
# TEST 6: GOOGLE LOGIN (check endpoint exists)
# ============================================
def test_google_login():
    print_test("Google Login Endpoint", "POST", "/google-login")
    
    # This will fail without real Google token, but checks if endpoint exists
    payload = {
        "idToken": "fake_google_token_for_testing"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/google-login", json=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code in [400, 401]:
            print_result(True, "Endpoint exists (rejected fake token as expected)", 
                        {"note": "Need real Google OAuth token to test fully"})
            return True
        elif response.status_code == 404:
            print_result(False, "Endpoint not found")
            return False
        else:
            data = response.json() if response.content else {}
            print_result(False, "Unexpected response", data)
            return False
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

# ============================================
# RUN ALL TESTS
# ============================================
def run_all_auth_tests():
    print("\n" + "="*60)
    print("🔐 AUTHENTICATION ENDPOINTS TEST SUITE")
    print("="*60)
    print(f"Base URL: {BASE_URL}")
    print(f"Test Time: {datetime.now()}")
    
    results = {
        "passed": 0,
        "failed": 0,
        "total": 0
    }
    
    # Test 1: Register
    print("\n📝 PHASE 1: USER REGISTRATION")
    success, email, password = test_register()
    results["total"] += 1
    if success:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 2: Login (with registered user or default)
    print("\n🔑 PHASE 2: USER LOGIN")
    login_success, login_data = test_login(email, password)
    results["total"] += 1
    if login_success:
        results["passed"] += 1
        token = None
        if login_data:
            token = login_data.get('idToken') or login_data.get('token') or login_data.get('accessToken')
    else:
        results["failed"] += 1
        token = None
    
    # Test 3: Profile (with token if available)
    print("\n👤 PHASE 3: USER PROFILE")
    profile_success = test_profile(token)
    results["total"] += 1
    if profile_success:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 4: Verify
    print("\n✉️ PHASE 4: EMAIL VERIFICATION")
    verify_success = test_verify(email)
    results["total"] += 1
    if verify_success:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 5: Forgot Password
    print("\n🔒 PHASE 5: FORGOT PASSWORD")
    forgot_success = test_forgot_password(email)
    results["total"] += 1
    if forgot_success:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 6: Google Login
    print("\n🌐 PHASE 6: GOOGLE LOGIN")
    google_success = test_google_login()
    results["total"] += 1
    if google_success:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Print summary
    print("\n" + "="*60)
    print("📊 AUTHENTICATION TEST SUMMARY")
    print("="*60)
    print(f"Total Tests: {results['total']}")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"Success Rate: {(results['passed']/results['total']*100):.1f}%")
    print("="*60)
    
    return results

if __name__ == "__main__":
    results = run_all_auth_tests()
    
    if results["failed"] > 0:
        exit(1)
    else:
        print("\n🎉 ALL AUTHENTICATION TESTS PASSED!")
        exit(0)
