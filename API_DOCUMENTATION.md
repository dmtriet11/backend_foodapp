# Backend Food App - Complete API Documentation

## Table of Contents
1. [User Authentication & Management](#user-authentication--management)
2. [Food & Restaurant Endpoints](#food--restaurant-endpoints)
3. [Chatbot Endpoints](#chatbot-endpoints)
4. [Map & Routing Endpoints](#map--routing-endpoints)

---

## Base URL
All endpoints are prefixed with `/api`

```
http://localhost:5000/api
```

---

## User Authentication & Management

### 1. Register New User
**Endpoint:** `POST /api/register`

**Description:** Create a new user account and send verification email.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe"
}
```

**Validation:**
- Email must be valid format
- Password must be at least 6 characters
- All fields are required

**Success Response (200):**
```json
{
  "message": "Đăng ký thành công! Mã xác thực đã được gửi đến email của bạn.",
  "user": {
    "uid": "firebase_uid",
    "name": "John Doe",
    "email": "user@example.com",
    "avatar_url": "",
    "favorites": [],
    "history": [],
    "location": {}
  }
}
```

**Error Responses:**
- `400` - Missing information, invalid email, password too short, or email sending failed
- `400` - Email already exists

---

### 2. Login
**Endpoint:** `POST /api/login`

**Description:** Authenticate user with email and password.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Success Response (200):**
```json
{
  "message": "Đăng nhập thành công!",
  "user": {
    "uid": "firebase_uid",
    "name": "John Doe",
    "email": "user@example.com",
    "avatar_url": "https://...",
    "favorites": ["1", "2", "3"],
    "history": [],
    "location": {}
  },
  "idToken": "firebase_id_token"
}
```

**Error Responses:**
- `400` - Missing email or password
- `401` - Wrong email or password
- `403` - Email not verified
- `404` - Email doesn't exist

**Note:** Store the `idToken` for authenticated requests.

---

### 3. Google Login
**Endpoint:** `POST /api/google-login`

**Description:** Authenticate user with Google OAuth token.

**Request Body:**
```json
{
  "idToken": "google_oauth_token"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Đăng nhập Google thành công!",
  "user": {
    "uid": "firebase_uid",
    "name": "John Doe",
    "email": "user@example.com",
    "avatar_url": "https://lh3.googleusercontent.com/...",
    "favorites": [],
    "history": [],
    "location": {}
  }
}
```

**Error Responses:**
- `400` - Missing idToken
- `401` - Token invalid or expired

---

### 4. Verify Email
**Endpoint:** `POST /api/verify`

**Description:** Verify user email with verification code sent via email.

**Request Body:**
```json
{
  "email": "user@example.com",
  "code": "123456"
}
```

**Success Response (200):**
```json
{
  "message": "Xác thực email thành công!"
}
```

**Error Responses:**
- `400` - Missing email or code, or code incorrect

---

### 5. Get User Profile
**Endpoint:** `GET /api/profile`

**Description:** Get current user's profile information.

**Authentication:** Required (JWT token in Authorization header)

**Headers:**
```
Authorization: Bearer <idToken>
```

**Success Response (200):**
```json
{
  "message": "Lấy thông tin người dùng thành công.",
  "user": {
    "uid": "firebase_uid",
    "name": "John Doe",
    "email": "user@example.com",
    "avatar_url": "https://...",
    "favorites": ["1", "2"],
    "history": [],
    "location": {}
  }
}
```

**Error Responses:**
- `401` - Unauthorized (invalid or missing token)
- `404` - User not found in database

---

### 6. Update Profile
**Endpoint:** `POST /api/user/update-profile`

**Description:** Update user profile information (name and avatar).

**Request Body:**
```json
{
  "uid": "firebase_uid",
  "name": "New Name",
  "avatar_url": "https://new-avatar-url.com/image.jpg"
}
```

**Success Response (200):**
```json
{
  "message": "Cập nhật hồ sơ thành công!",
  "user": {
    "uid": "firebase_uid",
    "name": "New Name",
    "email": "user@example.com",
    "avatar_url": "https://new-avatar-url.com/image.jpg",
    "favorites": [],
    "history": [],
    "location": {}
  }
}
```

**Error Responses:**
- `400` - Missing UID
- `500` - Update failed

---

### 7. Update Password (While Logged In)
**Endpoint:** `POST /api/user/update-password`

**Description:** Change password when user is logged in.

**Request Body:**
```json
{
  "uid": "firebase_uid",
  "old_password": "oldpass123",
  "new_password": "newpass456"
}
```

**Validation:**
- New password must be at least 6 characters

**Success Response (200):**
```json
{
  "message": "Đổi mật khẩu thành công!"
}
```

**Error Responses:**
- `400` - Missing fields or password too short
- `401` - Old password incorrect
- `404` - Email not found

---

### 8. Update Email
**Endpoint:** `POST /api/user/update-email`

**Description:** Change user's email address (requires password verification).

**Request Body:**
```json
{
  "uid": "firebase_uid",
  "password": "current_password",
  "new_email": "newemail@example.com"
}
```

**Success Response (200):**
```json
{
  "message": "Đổi email thành công! Vui lòng kiểm tra email mới để lấy mã xác thực.",
  "require_verify": true
}
```

**Error Responses:**
- `400` - Missing info, email same as current, or email already in use
- `401` - Password incorrect

---

### 9. Forgot Password
**Endpoint:** `POST /api/forgot-password`

**Description:** Request password reset code via email.

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Success Response (200):**
```json
{
  "message": "Mã xác thực đã được gửi đến email của bạn. Vui lòng kiểm tra hộp thư."
}
```

**Error Responses:**
- `400` - Missing email
- `404` - Email not registered
- `500` - Email sending failed

---

### 10. Change Password (With Verification Code)
**Endpoint:** `POST /api/change-password`

**Description:** Reset password using verification code from email.

**Request Body:**
```json
{
  "email": "user@example.com",
  "code": "123456",
  "new_password": "newpassword123"
}
```

**Validation:**
- New password must be at least 6 characters

**Success Response (200):**
```json
{
  "message": "Đổi mật khẩu thành công! Bạn có thể đăng nhập bằng mật khẩu mới."
}
```

**Error Responses:**
- `400` - Missing fields, password too short, or code incorrect
- `404` - Email not found

---

### 11. Toggle Restaurant Favorite
**Endpoint:** `POST /api/favorite/toggle-restaurant`

**Description:** Add or remove restaurant from user's favorites.

**Authentication:** Required (JWT token in Authorization header)

**Headers:**
```
Authorization: Bearer <idToken>
```

**Request Body:**
```json
{
  "restaurant_id": "123"
}
```

**Success Response (200):**
```json
{
  "message": "Đã thêm nhà hàng vào danh sách yêu thích.",
  "action": "added",
  "favorites": ["123", "456", "789"]
}
```

Or when removing:
```json
{
  "message": "Đã xóa nhà hàng khỏi danh sách yêu thích.",
  "action": "removed",
  "favorites": ["456", "789"]
}
```

**Error Responses:**
- `400` - Missing restaurant_id
- `401` - Unauthorized
- `404` - User not found

---

### 12. View Favorites
**Endpoint:** `GET /api/favorite/view`

**Description:** Get list of user's favorite restaurant IDs.

**Authentication:** Required (JWT token in Authorization header)

**Headers:**
```
Authorization: Bearer <idToken>
```

**Success Response (200):**
```json
{
  "user_id": "firebase_uid",
  "favorites": ["1", "2", "3", "5", "10"]
}
```

**Error Responses:**
- `401` - Unauthorized
- `404` - User not found

---

## Food & Restaurant Endpoints

### 13. Get All Restaurants
**Endpoint:** `GET /api/restaurants`

**Description:** Retrieve all restaurants from the database.

**Success Response (200):**
```json
{
  "success": true,
  "count": 150,
  "restaurants": [
    {
      "id": "1",
      "name": "Phở Hà Nội",
      "address": "123 Nguyễn Huệ, Quận 1, TP.HCM",
      "lat": 10.7769,
      "lon": 106.7009,
      "rating": 4.5,
      "category_id": 2,
      "price_range": "50,000đ-150,000đ",
      "phone_number": "0901234567",
      "open_hours": "6:00 - 22:00",
      "main_image_url": "https://...",
      "tags": ["phở", "món Bắc", "bữa sáng"]
    }
  ]
}
```

---

### 14. Search Restaurants (Simple)
**Endpoint:** `GET /api/restaurants/search?q=<query>`

**Description:** Simple search by restaurant name or address.

**Query Parameters:**
- `q` (string): Search query

**Example:** `/api/restaurants/search?q=phở`

**Success Response (200):**
```json
{
  "success": true,
  "count": 15,
  "restaurants": [...]
}
```

---

### 15. Advanced Search
**Endpoint:** `POST /api/search`

**Description:** Advanced search with multiple filters and location-based search.

**Request Body:**
```json
{
  "query": "phở",
  "province": "Hồ Chí Minh",
  "lat": 10.7769,
  "lon": 106.7009,
  "radius": 5000,
  "categories": [1, 2],
  "min_price": 50000,
  "max_price": 200000,
  "min_rating": 4.0,
  "max_rating": 5.0,
  "tags": ["bữa sáng", "món Bắc"]
}
```

**Parameters:**
- `query` (string, optional): Search keyword
- `province` (string, optional): Filter by province/city
- `lat`, `lon` (float, optional): User location for distance calculation
- `radius` (float, optional): Search radius in meters (auto-converted to km if > 50)
- `categories` (array, optional): Category IDs to filter
- `min_price`, `max_price` (int, optional): Price range in VND
- `min_rating`, `max_rating` (float, optional): Rating range (0-5)
- `tags` (array, optional): Tags to filter by

**Success Response (200):**
```json
{
  "success": true,
  "total": 25,
  "places": [
    {
      "id": "1",
      "name": "Phở Hà Nội",
      "address": "123 Nguyễn Huệ, Quận 1, TP.HCM",
      "position": {
        "lat": 10.7769,
        "lon": 106.7009
      },
      "dishType": "soup",
      "pinColor": "blue",
      "rating": 4.5,
      "price_range": "50,000đ-150,000đ",
      "phone_number": "0901234567",
      "open_hours": "6:00 - 22:00",
      "main_image_url": "https://...",
      "tags": ["phở", "món Bắc"],
      "distance": 2.5
    }
  ]
}
```

**Note:** Distance is only included when lat/lon are provided.

---

### 16. Get Restaurant Details
**Endpoint:** `GET /api/restaurants/<restaurant_id>`

**Description:** Get detailed information about a specific restaurant including its menu.

**Example:** `/api/restaurants/1`

**Success Response (200):**
```json
{
  "id": "1",
  "name": "Phở Hà Nội",
  "address": "123 Nguyễn Huệ, Quận 1, TP.HCM",
  "lat": 10.7769,
  "lon": 106.7009,
  "rating": 4.5,
  "category_id": 2,
  "price_range": "50,000đ-150,000đ",
  "phone_number": "0901234567",
  "open_hours": "6:00 - 22:00",
  "main_image_url": "https://...",
  "tags": ["phở", "món Bắc"],
  "menu": [
    {
      "id": "1",
      "restaurant_id": "1",
      "dish_name": "Phở Bò",
      "price": "80,000đ",
      "description": "Phở bò truyền thống Hà Nội",
      "dish_tags": ["phở", "bò"]
    }
  ]
}
```

**Error Responses:**
- `404` - Restaurant not found

---

### 17. Get Restaurants by IDs
**Endpoint:** `POST /api/restaurants/details-by-ids`

**Description:** Fetch details for multiple restaurants at once (useful for favorites).

**Request Body:**
```json
{
  "ids": ["1", "2", "5", "10"]
}
```

**Success Response (200):**
```json
{
  "success": true,
  "restaurants": [...],
  "count": 4
}
```

**Note:** Empty array returns successfully with count 0.

---

### 18. Get Nearby Restaurants
**Endpoint:** `GET /api/restaurants/nearby?latitude=<lat>&longitude=<lon>&radius=<radius>`

**Description:** Find restaurants near a specific location.

**Query Parameters:**
- `latitude` (float, required): User's latitude
- `longitude` (float, required): User's longitude
- `radius` (float, optional): Search radius in meters (default: 5000m)

**Example:** `/api/restaurants/nearby?latitude=10.7769&longitude=106.7009&radius=3000`

**Success Response (200):**
```json
{
  "success": true,
  "count": 20,
  "restaurants": [
    {
      "id": "1",
      "name": "Phở Hà Nội",
      "address": "123 Nguyễn Huệ, Quận 1, TP.HCM",
      "distance": 1.5,
      "rating": 4.5,
      "price_range": "50,000đ-150,000đ",
      ...
    }
  ]
}
```

**Note:** Results are sorted by distance (closest first).

**Error Responses:**
- `400` - Missing latitude or longitude

---

### 19. Get Restaurants by Category
**Endpoint:** `GET /api/restaurants/category/<category_id>`

**Description:** Get all restaurants in a specific category.

**Example:** `/api/restaurants/category/2`

**Success Response (200):**
```json
{
  "success": true,
  "count": 30,
  "restaurants": [...]
}
```

---

### 20. Get All Categories
**Endpoint:** `GET /api/categories`

**Description:** Get list of all food categories.

**Success Response (200):**
```json
{
  "success": true,
  "count": 5,
  "categories": [
    {
      "id": 1,
      "name": "Món Khô",
      "description": "Các món ăn khô như cơm, bún, mì",
      "dishType": "dry",
      "pinColor": "red"
    },
    {
      "id": 2,
      "name": "Món Nước",
      "description": "Các món ăn có nước như phở, hủ tiếu",
      "dishType": "soup",
      "pinColor": "blue"
    },
    {
      "id": 3,
      "name": "Món Chay",
      "description": "Các món ăn chay",
      "dishType": "vegetarian",
      "pinColor": "green"
    },
    {
      "id": 4,
      "name": "Món Mặn",
      "description": "Các món ăn mặn",
      "dishType": "salty",
      "pinColor": "orange"
    },
    {
      "id": 5,
      "name": "Hải Sản",
      "description": "Các món hải sản",
      "dishType": "seafood",
      "pinColor": "purple"
    }
  ]
}
```

---

### 21. Get Category Details
**Endpoint:** `GET /api/categories/<category_id>`

**Description:** Get details of a specific category.

**Example:** `/api/categories/2`

**Success Response (200):**
```json
{
  "id": 2,
  "name": "Món Nước",
  "description": "Các món ăn có nước như phở, hủ tiếu",
  "dishType": "soup",
  "pinColor": "blue"
}
```

**Error Responses:**
- `404` - Category not found

---

### 22. Get All Foods (Menu Items)
**Endpoint:** `GET /api/foods?limit=<limit>`

**Description:** Get list of menu items/dishes.

**Query Parameters:**
- `limit` (int, optional): Max number of items to return (default: 50)

**Example:** `/api/foods?limit=100`

**Success Response (200):**
```json
{
  "success": true,
  "count": 50,
  "foods": [
    {
      "id": "1",
      "restaurant_id": "1",
      "dish_name": "Phở Bò",
      "price": "80,000đ",
      "description": "Phở bò truyền thống Hà Nội",
      "dish_tags": ["phở", "bò"]
    }
  ]
}
```

---

### 23. Get Food Details
**Endpoint:** `GET /api/foods/<food_id>`

**Description:** Get details of a specific menu item.

**Example:** `/api/foods/123`

**Success Response (200):**
```json
{
  "id": "123",
  "restaurant_id": "1",
  "dish_name": "Phở Bò",
  "price": "80,000đ",
  "description": "Phở bò truyền thống Hà Nội",
  "dish_tags": ["phở", "bò"],
  "category_id": 2
}
```

**Error Responses:**
- `404` - Food not found

---

### 24. Search Foods
**Endpoint:** `GET /api/foods/search?q=<query>`

**Description:** Search for dishes by name.

**Query Parameters:**
- `q` (string): Search query

**Example:** `/api/foods/search?q=phở`

**Success Response (200):**
```json
{
  "success": true,
  "count": 15,
  "foods": [...]
}
```

---

### 25. Get Foods by Category
**Endpoint:** `GET /api/foods/category/<category_id>`

**Description:** Get all dishes in a specific category.

**Example:** `/api/foods/category/2`

**Success Response (200):**
```json
{
  "success": true,
  "count": 40,
  "foods": [...]
}
```

---

### 26. Get Foods by Restaurant
**Endpoint:** `GET /api/foods/restaurant/<restaurant_id>`

**Description:** Get all menu items for a specific restaurant.

**Example:** `/api/foods/restaurant/1`

**Success Response (200):**
```json
{
  "success": true,
  "count": 15,
  "foods": [
    {
      "id": "1",
      "restaurant_id": "1",
      "dish_name": "Phở Bò",
      "price": "80,000đ",
      "description": "Phở bò truyền thống Hà Nội",
      "dish_tags": ["phở", "bò"]
    }
  ]
}
```

---

### 27. Get Directions
**Endpoint:** `POST /api/direction`

**Description:** Get route directions between two locations using OSRM (OpenStreetMap).

**Request Body:**
```json
{
  "origin": {
    "lat": 10.7769,
    "lon": 106.7009
  },
  "destination": {
    "lat": 10.7553,
    "lon": 106.6715
  },
  "mode": "driving"
}
```

**Parameters:**
- `origin` (object, required): Starting location
- `destination` (object, required): Ending location
- `mode` (string, optional): Travel mode - "driving" (default), "walking", or "bicycling"

**Success Response (200):**
```json
{
  "distance_meters": 5432.5,
  "duration_seconds": 780,
  "overview_polyline": "encoded_polyline_string",
  "legs": [
    {
      "steps": [...],
      "start_address": "Vị trí xuất phát",
      "end_address": "Điểm đến"
    }
  ]
}
```

**Error Responses:**
- `400` - Missing origin or destination, or route not found
- `502` - OSRM service connection error

---

### 28. Create Review
**Endpoint:** `POST /api/reviews`

**Description:** Submit a review for a restaurant with rating and comment.

**Authentication:** Required (JWT token in Authorization header)

**Headers:**
```
Authorization: Bearer <idToken>
```

**Request Body:**
```json
{
  "target_id": "1",
  "rating": 5,
  "comment": "Rất ngon và phục vụ tốt!",
  "type": "restaurant"
}
```

**Parameters:**
- `target_id` (string, required): Restaurant ID
- `rating` (int, required): Rating from 1 to 5
- `comment` (string, optional): Review text
- `type` (string, required): Must be "restaurant"

**Success Response (201):**
```json
{
  "message": "Đánh giá của bạn đã được gửi thành công.",
  "review": {
    "id": "1_user123_1234567890",
    "user_id": "user123",
    "username": "John Doe",
    "avatar_url": "https://...",
    "target_id": "1",
    "type": "restaurant",
    "rating": 5,
    "comment": "Rất ngon và phục vụ tốt!",
    "timestamp": 1234567890000,
    "date": "08/12/2025",
    "new_restaurant_rating": 4.7
  }
}
```

**Note:** The system uses weighted average rating that combines original ratings with new user reviews.

**Error Responses:**
- `400` - Missing required fields or invalid rating
- `401` - Unauthorized

---

### 29. Get Restaurant Reviews
**Endpoint:** `GET /api/reviews/restaurant/<restaurant_id>`

**Description:** Get reviews for a specific restaurant (20 most recent).

**Example:** `/api/reviews/restaurant/1`

**Success Response (200):**
```json
{
  "success": true,
  "count": 15,
  "reviews": [
    {
      "id": "1_user123_1234567890",
      "user_id": "user123",
      "username": "John Doe",
      "avatar_url": "https://...",
      "target_id": "1",
      "type": "restaurant",
      "rating": 5,
      "comment": "Rất ngon và phục vụ tốt!",
      "timestamp": 1234567890000,
      "date": "08/12/2025"
    }
  ],
  "current_rating": 4.7
}
```

**Note:** Reviews are sorted by most recent first. Only returns the 20 latest reviews for performance.

---

### 30. Get Restaurant Rating
**Endpoint:** `GET /api/rating/<restaurant_id>`

**Description:** Get the current weighted average rating for a restaurant.

**Example:** `/api/rating/1`

**Success Response (200):**
```json
{
  "success": true,
  "rating": 4.7
}
```

**Note:** If no user reviews exist, returns the original rating from static data.

---

### 31. Delete Review
**Endpoint:** `DELETE /api/reviews/<review_id>`

**Description:** Delete a review (only the creator can delete their own review).

**Authentication:** Required (JWT token in Authorization header)

**Headers:**
```
Authorization: Bearer <idToken>
```

**Example:** `/api/reviews/1_user123_1234567890`

**Success Response (200):**
```json
{
  "message": "Đã xóa đánh giá thành công.",
  "new_restaurant_rating": 4.5
}
```

**Error Responses:**
- `400` - Invalid review_id format
- `401` - Unauthorized (not logged in)
- `403` - Forbidden (not the review owner)
- `404` - Review not found

**Note:** After deletion, the restaurant's weighted rating is automatically recalculated.

---

## Chatbot Endpoints

### 32. Chat with Bot
**Endpoint:** `POST /api/chat`

**Description:** Send a message to the AI chatbot for food recommendations and information.

**Request Body:**
```json
{
  "message": "Tìm quán phở ngon ở Hà Nội",
  "conversation_id": "optional_conversation_id"
}
```

**Parameters:**
- `message` or `query` (string, required): User's message
- `conversation_id` (string, optional): ID to maintain conversation context. If not provided, a new conversation is created.

**Success Response (200):**
```json
{
  "conversation_id": "uuid-string",
  "user_message": "Tìm quán phở ngon ở Hà Nội",
  "bot_response": "Dưới đây là các quán phở ngon ở Hà Nội:\n\n1. Phở Hà Nội\n📍 123 Nguyễn Huệ, Quận 1\n⭐ Rating: 4.5/5\n📞 0901234567\n🕒 6:00 - 22:00\n💰 50,000đ-150,000đ",
  "timestamp": "2025-12-08T10:30:00.000Z"
}
```

**Features:**
- Natural language understanding for restaurant search
- Searches by:
  - Dish name (e.g., "phở", "bún bò")
  - Restaurant name
  - Location (e.g., "Hồ Chí Minh", "gần tôi")
  - Combinations (e.g., "phở ở Hà Nội")
- Filters by price (e.g., "giá rẻ")
- Filters by rating (e.g., "ngon nhất", "đánh giá cao")
- Maintains conversation context using `conversation_id`
- Returns formatted recommendations with details

**Error Responses:**
- `400` - Missing message
- `500` - API key not configured or OpenAI API error
- `504` - Request timeout

---

### 32. Get Chat History
**Endpoint:** `GET /api/chat/history/<conversation_id>`

**Description:** Retrieve conversation history for a specific conversation.

**Example:** `/api/chat/history/uuid-string`

**Success Response (200):**
```json
{
  "conversation_id": "uuid-string",
  "history": [
    {
      "user_message": "Tìm quán phở",
      "bot_response": "Dưới đây là các quán phở...",
      "timestamp": "2025-12-08T10:30:00.000Z",
      "search_type": "dish_only",
      "restaurants_found": 15,
      "restaurant_names": ["Phở Hà Nội", "Phở 24", "Phở Gia Truyền"]
    }
  ],
  "total_messages": 1
}
```

---

### 33. Check Chatbot Status
**Endpoint:** `GET /api/chat/status`

**Description:** Check if chatbot is running and configured properly.

**Success Response (200):**
```json
{
  "status": "running",
  "api_key_configured": true,
  "total_conversations": 5,
  "total_restaurants": 150,
  "timestamp": "2025-12-08T10:30:00.000Z"
}
```

---

## Map & Routing Endpoints

### 35. Filter Map Markers
**Endpoint:** `POST /api/map/filter`

**Description:** Filter restaurants on map by various criteria including location, category, price, rating, and tags.

**Request Body:**
```json
{
  "lat": 10.7769,
  "lon": 106.7009,
  "radius": 2,
  "categories": [1, 2, 3],
  "min_price": 50000,
  "max_price": 200000,
  "min_rating": 4.0,
  "max_rating": 5.0,
  "tags": ["bữa sáng"],
  "limit": 50
}
```

**Parameters:**
- `lat`, `lon` (float, optional): User's current location
- `radius` (float, optional): Search radius in km (default: 2)
- `categories` (array, optional): Category IDs to filter
  - `null` = no filter (show all)
  - `[]` = strict filter (empty result)
  - `[1,2,3]` = show only these categories
- `min_price`, `max_price` (int, optional): Price range in VND
- `min_rating`, `max_rating` (float, optional): Rating range (default: 0-5)
- `tags` (array, optional): Tags to filter by
- `limit` (int, optional): Max results (default: no limit)

**Success Response (200):**
```json
{
  "success": true,
  "total": 25,
  "places": [
    {
      "id": "1",
      "name": "Phở Hà Nội",
      "address": "123 Nguyễn Huệ, Quận 1, TP.HCM",
      "position": {
        "lat": 10.7769,
        "lon": 106.7009
      },
      "dishType": "soup",
      "pinColor": "blue",
      "rating": 4.5,
      "price_range": "50,000đ-150,000đ",
      "phone_number": "0901234567",
      "open_hours": "6:00 - 22:00",
      "main_image_url": "https://...",
      "tags": ["phở", "món Bắc"],
      "distance": 1.5
    }
  ],
  "filters_applied": {
    "has_location": true,
    "radius_km": 2,
    "categories": [1, 2, 3],
    "min_price": 50000,
    "max_price": 200000,
    "min_rating": 4.0,
    "max_rating": 5.0,
    "tags": ["bữa sáng"]
  }
}
```

**Note:** Results are sorted by distance when location is provided.

---

### 36. Get Route Between Points
**Endpoint:** `POST /api/get-route`

**Description:** Calculate route coordinates between two points using TomTom routing service.

**Request Body:**
```json
{
  "start_lat": 10.7769,
  "start_lon": 106.7009,
  "end_lat": 10.7553,
  "end_lon": 106.6715
}
```

**Parameters:**
- `start_lat`, `start_lon` (float, required): Starting coordinates
- `end_lat`, `end_lon` (float, required): Ending coordinates

**Success Response (200):**
```json
{
  "success": true,
  "message": "Route calculated with 150 points",
  "coordinates": [
    {
      "latitude": 10.7769,
      "longitude": 106.7009
    },
    {
      "latitude": 10.7768,
      "longitude": 106.7010
    }
  ],
  "total_points": 150
}
```

**Error Responses:**
- `400` - Missing required fields, invalid coordinates, or start/end too close
- `500` - Route calculation error

---

## Data Models

### User Object
```json
{
  "uid": "string",
  "name": "string",
  "email": "string",
  "avatar_url": "string",
  "favorites": ["restaurant_id_1", "restaurant_id_2"],
  "history": [],
  "location": {}
}
```

### Restaurant Object
```json
{
  "id": "string",
  "name": "string",
  "address": "string",
  "lat": "float",
  "lon": "float",
  "rating": "float",
  "category_id": "int",
  "price_range": "string",
  "phone_number": "string",
  "open_hours": "string",
  "main_image_url": "string",
  "tags": ["string"]
}
```

### Menu Item Object
```json
{
  "id": "string",
  "restaurant_id": "string",
  "dish_name": "string",
  "price": "string",
  "description": "string",
  "dish_tags": ["string"],
  "category_id": "int"
}
```

### Review Object
```json
{
  "id": "string",
  "user_id": "string",
  "username": "string",
  "avatar_url": "string",
  "target_id": "string",
  "type": "string",
  "rating": "int (1-5)",
  "comment": "string",
  "timestamp": "int",
  "date": "string"
}
```

---

## Authentication

Most user-specific endpoints require authentication using Firebase JWT tokens.

**Header Format:**
```
Authorization: Bearer <idToken>
```

**Getting the Token:**
- Login endpoint (`/api/login`) returns `idToken`
- Google login endpoint (`/api/google-login`) provides authentication
- Store token securely and include in subsequent requests

**Authenticated Endpoints:**
- `/api/profile` - GET user profile
- `/api/favorite/toggle-restaurant` - Manage favorites
- `/api/favorite/view` - View favorites
- `/api/reviews` - Create reviews

---

## Error Handling

### Standard Error Response Format
```json
{
  "error": "Error message description"
}
```

### Common HTTP Status Codes
- `200` - Success
- `201` - Created (for new resources)
- `400` - Bad Request (validation errors, missing parameters)
- `401` - Unauthorized (authentication required or failed)
- `403` - Forbidden (email not verified, etc.)
- `404` - Not Found (resource doesn't exist)
- `500` - Internal Server Error
- `502` - Bad Gateway (external service error)
- `504` - Gateway Timeout

---

## Category Mapping

### Category IDs
- `1` - Món Khô (Dry) - Red pin
- `2` - Món Nước (Soup) - Blue pin
- `3` - Món Chay (Vegetarian) - Green pin
- `4` - Món Mặn (Salty) - Orange pin
- `5` - Hải Sản (Seafood) - Purple pin

### Dish Type to Pin Color
```json
{
  "dry": "red",
  "soup": "blue",
  "vegetarian": "green",
  "salty": "orange",
  "seafood": "purple"
}
```

---

## Notes

### Price Range Format
Price ranges are formatted as strings: `"50,000đ-150,000đ"` or `"300,000đ+"`

### Distance Calculation
- Uses Haversine formula for accurate distance calculation
- Distances are in kilometers (km)
- Radius parameters in meters are auto-converted to km if > 50

### Rating System
- Original ratings from static data: weighted with factor N_MIN=10
- New user reviews: weighted equally
- Formula: `(source_rating * 10 + sum(user_ratings)) / (10 + count(user_ratings))`

### Search Algorithm
The advanced search (`/api/search`) implements sophisticated filtering:
1. Text search in restaurant names and menu items
2. Location-based filtering with radius
3. Category filtering
4. Price range filtering (checks overlap)
5. Rating filtering
6. Tag-based filtering
7. Distance calculation and sorting

### Chatbot Intelligence
The chatbot uses OpenAI GPT-4o-mini with:
- Context-aware responses
- Multi-criteria search (location, dish, restaurant name)
- Price and rating filtering detection
- Conversation memory (last 10 messages)
- Vietnamese language support
- Smart sorting based on user intent

---

## Environment Variables

Required environment variables:
```
OPENAI_API_KEY=sk-...
GOOGLE_CLIENT_ID=...
FIREBASE_API_KEY=...
```

---

## Rate Limits

- No explicit rate limits currently implemented
- Chatbot limited to 600 tokens per response
- Reviews: 20 most recent per restaurant
- Foods listing: Default 50 items (configurable with limit parameter)

---

## Support

For issues or questions, please check:
- AUTH_API.md - Detailed authentication documentation
- CHATBOT_API.md - Detailed chatbot documentation
- database_overview.md - Database structure documentation

---

**Last Updated:** December 8, 2025
**API Version:** 1.0
**Backend Framework:** Flask with Firebase
