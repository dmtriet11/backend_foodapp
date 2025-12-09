"""
🧪 COMPREHENSIVE API TEST SUITE
Test tất cả 37 endpoints của Food App Backend
"""

import requests
import json
from datetime import datetime

# ============================================
# CẤU HÌNH
# ============================================
BASE_URL = "https://backend-foodapp-1-wr4a.onrender.com/api"
# Hoặc cho local: BASE_URL = "http://localhost:5000/api"

# Test credentials (cần tạo account trước)
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "Test123456"

# ============================================
# HELPER FUNCTIONS
# ============================================

def print_test(name, method, endpoint):
    """Print test header"""
    print(f"\n{'='*60}")
    print(f"🧪 Test: {name}")
    print(f"   Method: {method}")
    print(f"   Endpoint: {endpoint}")
    print(f"{'='*60}")

def print_result(success, message, data=None):
    """Print test result"""
    icon = "✅" if success else "❌"
    print(f"{icon} {message}")
    if data and len(str(data)) < 500:
        print(f"   Response: {data}")
    elif data:
        print(f"   Response: [Data too long, showing length: {len(str(data))} chars]")

# ============================================
# TEST FUNCTIONS
# ============================================

def test_root():
    """Test root endpoint"""
    print_test("Root Endpoint", "GET", "/")
    try:
        response = requests.get(f"{BASE_URL[:-4]}/")
        if response.status_code == 200:
            print_result(True, "Root endpoint OK", response.json())
            return True
        else:
            print_result(False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

# ============================================
# RESTAURANT ENDPOINTS
# ============================================

def test_get_restaurants():
    """Test GET /restaurants"""
    print_test("Get All Restaurants", "GET", "/restaurants")
    try:
        response = requests.get(f"{BASE_URL}/restaurants")
        if response.status_code == 200:
            data = response.json()
            count = data.get('count', 0)
            print_result(True, f"Got {count} restaurants")
            return True
        else:
            print_result(False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

def test_get_restaurant_detail():
    """Test GET /restaurants/<place_id> - using Google Places ID"""
    place_id = "ChIJEzXHbEcvdTERYJU-jigOumI"  # First restaurant ID from data
    print_test("Get Restaurant Detail", "GET", f"/restaurants/{place_id}")
    try:
        response = requests.get(f"{BASE_URL}/restaurants/{place_id}")
        if response.status_code == 200:
            data = response.json()
            print_result(True, f"Got restaurant: {data.get('name', 'Unknown')}")
            return True
        else:
            print_result(False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

def test_search_restaurants():
    """Test POST /search"""
    print_test("Search Restaurants", "POST", "/search")
    try:
        payload = {
            "query": "pizza",
            "lat": 10.7769,
            "lon": 106.7009,
            "radius": 5
        }
        response = requests.post(f"{BASE_URL}/search", json=payload)
        if response.status_code == 200:
            data = response.json()
            count = len(data.get('results', []))
            print_result(True, f"Found {count} results for 'pizza'")
            return True
        else:
            print_result(False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

def test_restaurants_by_ids():
    """Test POST /restaurants/details-by-ids"""
    print_test("Get Restaurants by IDs", "POST", "/restaurants/details-by-ids")
    try:
        payload = {
            "ids": ["ChIJSaRb1CYvdTERU8axGNdAFxE", "ChIJxQUjKtsudTERO_KVgjmipAk"]
        }
        response = requests.post(f"{BASE_URL}/restaurants/details-by-ids", json=payload)
        if response.status_code == 200:
            data = response.json()
            count = len(data.get('restaurants', []))
            print_result(True, f"Got {count} restaurants")
            return True
        else:
            print_result(False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

# ============================================
# FOOD ENDPOINTS
# ============================================

def test_get_foods():
    """Test GET /foods"""
    print_test("Get All Foods", "GET", "/foods")
    try:
        response = requests.get(f"{BASE_URL}/foods")
        if response.status_code == 200:
            data = response.json()
            count = data.get('count', 0)
            print_result(True, f"Got {count} foods")
            return True
        else:
            print_result(False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

def test_get_food_detail():
    """Test GET /foods/<id>"""
    print_test("Get Food Detail", "GET", "/foods/101")
    try:
        response = requests.get(f"{BASE_URL}/foods/101")
        if response.status_code == 200:
            data = response.json()
            print_result(True, f"Got food: {data.get('dish_name', 'Unknown')}")
            return True
        else:
            print_result(False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

# ============================================
# CATEGORY ENDPOINTS
# ============================================

def test_get_categories():
    """Test GET /categories"""
    print_test("Get All Categories", "GET", "/categories")
    try:
        response = requests.get(f"{BASE_URL}/categories")
        if response.status_code == 200:
            data = response.json()
            count = data.get('count', 0)
            print_result(True, f"Got {count} categories")
            return True
        else:
            print_result(False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

# ============================================
# MAP ENDPOINTS
# ============================================

def test_map_filter():
    """Test POST /map/filter"""
    print_test("Map Filter", "POST", "/map/filter")
    try:
        payload = {
            "lat": 10.7769,
            "lon": 106.7009,
            "radius": 2,
            "categories": [1, 2],
            "min_rating": 4.0
        }
        response = requests.post(f"{BASE_URL}/map/filter", json=payload)
        if response.status_code == 200:
            data = response.json()
            count = len(data.get('markers', []))
            print_result(True, f"Found {count} markers")
            return True
        else:
            print_result(False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

# ============================================
# CHATBOT ENDPOINTS
# ============================================

def test_chatbot():
    """Test POST /chat"""
    print_test("Chatbot", "POST", "/chat")
    try:
        payload = {
            "message": "Gợi ý quán pizza gần đây",
            "conversation_id": None
        }
        response = requests.post(f"{BASE_URL}/chat", json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            reply = data.get('reply', '')
            print_result(True, f"Bot replied: {reply[:100]}...")
            return True
        else:
            print_result(False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

def test_chatbot_status():
    """Test GET /chat/status"""
    print_test("Chatbot Status", "GET", "/chat/status")
    try:
        response = requests.get(f"{BASE_URL}/chat/status")
        if response.status_code == 200:
            data = response.json()
            print_result(True, "Chatbot status OK", data)
            return True
        else:
            print_result(False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

# ============================================
# AUTH ENDPOINTS (Optional - cần credentials)
# ============================================

def test_register():
    """Test POST /register"""
    print_test("Register New User", "POST", "/register")
    try:
        payload = {
            "email": f"test_{datetime.now().timestamp()}@example.com",
            "password": "Test123456",
            "displayName": "Test User"
        }
        response = requests.post(f"{BASE_URL}/register", json=payload)
        if response.status_code in [200, 201]:
            print_result(True, "Registration successful")
            return True
        else:
            print_result(False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

# ============================================
# RUN ALL TESTS
# ============================================

def run_all_tests():
    """Run all API tests"""
    print("\n" + "="*60)
    print("🚀 STARTING COMPREHENSIVE API TEST SUITE")
    print("="*60)
    print(f"Base URL: {BASE_URL}")
    print(f"Test Time: {datetime.now()}")
    
    results = {
        "passed": 0,
        "failed": 0,
        "total": 0
    }
    
    # List of all test functions
    tests = [
        # Core
        ("Root", test_root),
        
        # Restaurants
        ("Get Restaurants", test_get_restaurants),
        ("Restaurant Detail", test_get_restaurant_detail),
        ("Search Restaurants", test_search_restaurants),
        ("Restaurants by IDs", test_restaurants_by_ids),
        
        # Foods
        ("Get Foods", test_get_foods),
        ("Food Detail", test_get_food_detail),
        
        # Categories
        ("Get Categories", test_get_categories),
        
        # Map
        ("Map Filter", test_map_filter),
        
        # Chatbot
        ("Chatbot", test_chatbot),
        ("Chatbot Status", test_chatbot_status),
        
        # Auth (optional)
        # ("Register", test_register),
    ]
    
    # Run all tests
    for test_name, test_func in tests:
        results["total"] += 1
        try:
            if test_func():
                results["passed"] += 1
            else:
                results["failed"] += 1
        except Exception as e:
            print_result(False, f"Test crashed: {str(e)}")
            results["failed"] += 1
    
    # Print summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    print(f"Total Tests: {results['total']}")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"Success Rate: {(results['passed']/results['total']*100):.1f}%")
    print("="*60)
    
    return results

if __name__ == "__main__":
    results = run_all_tests()
    
    # Exit with error code if tests failed
    if results["failed"] > 0:
        exit(1)
    else:
        print("\n🎉 ALL TESTS PASSED!")
        exit(0)
