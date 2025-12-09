# 📋 DEPLOYMENT CHECKLIST - FOOD APP BACKEND API

## 🎯 TẤT CẢ API ENDPOINTS (37 endpoints)

### 🏠 **ROOT**
- `GET /` - Home endpoint, API info

---

## 👤 **USER AUTHENTICATION & PROFILE (13 endpoints)**

### Authentication
1. `POST /api/register` - Đăng ký tài khoản mới
2. `POST /api/login` - Đăng nhập
3. `POST /api/google-login` - Đăng nhập bằng Google
4. `POST /api/verify` - Xác thực email
5. `POST /api/forgot-password` - Quên mật khẩu

### Profile Management
6. `GET /api/profile` - Lấy thông tin profile
7. `POST /api/user/update-profile` - Cập nhật profile
8. `POST /api/user/update-email` - Cập nhật email
9. `POST /api/user/update-password` - Cập nhật mật khẩu
10. `POST /api/change-password` - Đổi mật khẩu

### Favorites
11. `POST /api/favorite/toggle-restaurant` - Thêm/xóa yêu thích
12. `GET /api/favorite/view` - Xem danh sách yêu thích

---

## 🍜 **FOOD & RESTAURANTS (16 endpoints)**

### Restaurants
13. `GET /api/restaurants` - Lấy danh sách tất cả nhà hàng
14. `GET /api/restaurants/search` - Tìm kiếm nhà hàng (query string)
15. `GET /api/restaurants/<int:restaurant_id>` - Chi tiết nhà hàng
16. `POST /api/restaurants/details-by-ids` - Lấy nhiều nhà hàng theo IDs
17. `GET /api/restaurants/nearby` - Nhà hàng gần đây
18. `GET /api/restaurants/category/<int:category_id>` - Nhà hàng theo category

### Foods/Menus
19. `GET /api/foods` - Danh sách tất cả món ăn
20. `GET /api/foods/<int:food_id>` - Chi tiết món ăn
21. `GET /api/foods/search` - Tìm kiếm món ăn
22. `GET /api/foods/category/<int:category_id>` - Món ăn theo category
23. `GET /api/foods/restaurant/<int:restaurant_id>` - Menu của nhà hàng

### Categories
24. `GET /api/categories` - Danh sách categories
25. `GET /api/categories/<int:category_id>` - Chi tiết category

### Search (Advanced)
26. `POST /api/search` - Tìm kiếm nâng cao với filters

### Reviews & Ratings
27. `POST /api/reviews` - Tạo đánh giá mới
28. `GET /api/reviews/restaurant/<restaurant_id>` - Xem đánh giá nhà hàng
29. `GET /api/rating/<restaurant_id>` - Lấy rating nhà hàng
30. `DELETE /api/reviews/<review_id>` - Xóa đánh giá

### Directions
31. `POST /api/direction` - Lấy hướng dẫn đường đi

---

## 🗺️ **MAP & LOCATION (2 endpoints)**

32. `POST /api/map/filter` - Lọc nhà hàng trên bản đồ
33. `POST /api/get-route` - Lấy route từ A đến B

---

## 🤖 **CHATBOT (3 endpoints)**

34. `POST /api/chat` - Chat với AI bot
35. `GET /api/chat/history/<conversation_id>` - Lịch sử chat
36. `GET /api/chat/status` - Trạng thái chatbot

---

## 📦 **DEPENDENCIES REQUIRED**

### Core
- Flask==3.1.2
- flask-cors==6.0.1
- python-dotenv==1.2.1
- gunicorn==21.2.0

### Firebase
- firebase-admin==7.1.0
- google-auth==2.42.1
- google-cloud-firestore==2.21.0

### HTTP & API
- requests==2.32.5
- httpx==0.28.1

### Authentication
- PyJWT==2.10.1
- cryptography==46.0.3

---

## 🔧 **QUY TRÌNH DEPLOY ĐẦY ĐỦ**

### ✅ **BƯỚC 1: CHUẨN BỊ CODE**

#### 1.1. Kiểm tra cấu trúc project
```
✓ App.py - Entry point
✓ requirements.txt - Dependencies đầy đủ
✓ Procfile - Web server config
✓ runtime.txt - Python version
✓ .gitignore - Bảo vệ sensitive files
✓ README.md - Documentation
```

#### 1.2. Kiểm tra tất cả imports trong App.py
```python
✓ from routes.food import food_bp
✓ from routes.user import user_bp
✓ from routes.chatbot import chatbot_bp
✓ from routes.map import map_bp
✓ All blueprints registered
```

#### 1.3. Verify tất cả routes được import
```bash
# Chạy lệnh này để kiểm tra
python -c "from App import app; print(len(app.url_map._rules))"
# Phải trả về > 37 routes
```

---

### ✅ **BƯỚC 2: KIỂM TRA LOCAL**

#### 2.1. Test local server
```bash
cd backend_foodapp
python App.py
```

#### 2.2. Test các endpoint chính
```bash
# Test GET endpoints
curl http://localhost:5000/
curl http://localhost:5000/api/restaurants
curl http://localhost:5000/api/foods
curl http://localhost:5000/api/categories

# Test POST endpoints (cần Postman/Thunder Client)
POST http://localhost:5000/api/search
POST http://localhost:5000/api/chat
POST http://localhost:5000/api/login
```

#### 2.3. Kiểm tra logs
```
✓ "✔️ KHỞI TẠO FIREBASE THÀNH CÔNG!"
✓ "ĐÃ TẢI restaurants.json (1458) phần tử"
✓ "✅ API key loaded successfully"
✓ Không có lỗi import
```

---

### ✅ **BƯỚC 3: CHUẨN BỊ ENVIRONMENT VARIABLES**

#### 3.1. Danh sách biến cần thiết
```env
# Google Services
GOOGLE_API_KEY=<your_key>

# Firebase
FIREBASE_DB_URL=<your_db_url>

# Email (for password reset)
SENDER_EMAIL=<your_email>
SENDER_APP_PASSWORD=<your_app_password>

# OpenAI (for chatbot)
OPENAI_API_KEY=<your_openai_key>

# Flask
FLASK_ENV=production
```

#### 3.2. Tạo Firebase Secret File
- Chuẩn bị nội dung `firebase_auth.json`
- **KHÔNG** commit file này lên Git

---

### ✅ **BƯỚC 4: DEPLOY LÊN RENDER**

#### 4.1. Tạo Web Service
1. Truy cập: https://render.com
2. Click **"New +"** → **"Web Service"**
3. Kết nối GitHub: `dmtriet11/backend_foodapp`
4. Branch: `main`

#### 4.2. Cấu hình Build Settings
```
Name: food-app-backend
Region: Singapore (gần Việt Nam nhất)
Branch: main
Root Directory: (để trống)
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn App:app
Instance Type: Free
```

#### 4.3. Thêm Environment Variables
Vào **Environment** tab, thêm từng biến:
```
GOOGLE_API_KEY=<value>
FIREBASE_DB_URL=<value>
SENDER_EMAIL=<value>
SENDER_APP_PASSWORD=<value>
OPENAI_API_KEY=<value>
FLASK_ENV=production
```

#### 4.4. Thêm Secret Files
1. Click **"Advanced"** → **"Secret Files"**
2. Add Secret File:
   - Filename: `firebase_auth.json`
   - Contents: <paste nội dung Firebase service account JSON>

#### 4.5. Deploy
- Click **"Create Web Service"**
- Đợi 3-5 phút
- Check logs để đảm bảo không có lỗi

---

### ✅ **BƯỚC 5: VERIFY DEPLOYMENT**

#### 5.1. Kiểm tra health check
```bash
curl https://your-app.onrender.com/
# Expect: {"status": "running", "message": "🍜 Food App Backend API"}
```

#### 5.2. Test các endpoint chính

**GET Endpoints:**
```bash
# Restaurants
curl https://your-app.onrender.com/api/restaurants
curl https://your-app.onrender.com/api/restaurants/1

# Foods
curl https://your-app.onrender.com/api/foods
curl https://your-app.onrender.com/api/categories
```

**POST Endpoints (dùng Postman):**
```json
// POST /api/search
{
  "query": "pizza",
  "lat": 10.7769,
  "lon": 106.7009,
  "radius": 5
}

// POST /api/chat
{
  "message": "Gợi ý quán ăn Nhật",
  "conversation_id": null
}

// POST /api/login
{
  "email": "test@example.com",
  "password": "password123"
}
```

#### 5.3. Kiểm tra logs trên Render
```
✓ Firebase initialized
✓ Data loaded successfully
✓ API key loaded
✓ No import errors
✓ Server running on port
```

---

### ✅ **BƯỚC 6: POST-DEPLOYMENT**

#### 6.1. Test Performance
- Cold start: ~30-50s (free tier)
- Warm requests: <2s
- Test với nhiều requests đồng thời

#### 6.2. Monitor Errors
- Check Render logs thường xuyên
- Set up error notifications (nếu cần)

#### 6.3. Update Frontend
```javascript
// Cập nhật API base URL trong frontend
const API_BASE_URL = "https://your-app.onrender.com/api";
```

#### 6.4. Test từ Mobile App
```javascript
// iOS/Android
await fetch('https://your-app.onrender.com/api/restaurants');
```

---

## 🔍 **TROUBLESHOOTING CHECKLIST**

### Lỗi thường gặp và cách fix:

#### ❌ "Module not found"
```bash
# Fix: Kiểm tra imports trong App.py
✓ Đảm bảo tất cả blueprints được import
✓ Check __init__.py trong mỗi folder
```

#### ❌ "Firebase initialization failed"
```bash
# Fix: 
✓ Kiểm tra firebase_auth.json trong Secret Files
✓ Verify FIREBASE_DB_URL trong Environment Variables
```

#### ❌ "API key không được cấu hình"
```bash
# Fix:
✓ Thêm OPENAI_API_KEY vào Environment Variables
✓ Restart service sau khi thêm
```

#### ❌ "Port already in use" (local)
```bash
# Fix:
✓ Kill process: lsof -ti:5000 | xargs kill (Mac/Linux)
✓ Hoặc đổi port trong App.py
```

#### ❌ "CORS errors"
```bash
# Fix:
✓ Đã có CORS(app) trong App.py
✓ Nếu vẫn lỗi, thêm origins cụ thể
```

---

## 📊 **VERIFICATION MATRIX**

Sau khi deploy, test theo bảng sau:

| Endpoint Category | Method | Status | Notes |
|------------------|--------|---------|-------|
| Root | GET | ✅ | API info |
| Restaurants | GET | ✅ | 1458 records |
| Foods | GET | ✅ | 7 records |
| Categories | GET | ✅ | 5 categories |
| Search | POST | ⏳ | Need request body |
| Reviews | POST | ⏳ | Need auth token |
| Chatbot | POST | ⏳ | Need OPENAI_API_KEY |
| Login | POST | ⏳ | Need valid credentials |
| Map Filter | POST | ⏳ | Need location data |

---

## 🎯 **DEPLOYMENT SUCCESS CRITERIA**

### Minimum Requirements (MVP):
- ✅ Root endpoint hoạt động
- ✅ GET /api/restaurants hoạt động
- ✅ GET /api/foods hoạt động
- ✅ GET /api/categories hoạt động
- ✅ Firebase connected
- ✅ No critical errors in logs

### Full Deployment:
- ✅ All 37 endpoints hoạt động
- ✅ POST endpoints trả về đúng data
- ✅ Authentication flow hoàn chỉnh
- ✅ Chatbot phản hồi chính xác
- ✅ Search với filters hoạt động
- ✅ Reviews system functional
- ✅ Map filtering accurate

---

## 📝 **MAINTENANCE CHECKLIST**

### Hàng ngày:
- [ ] Check Render logs cho errors
- [ ] Monitor response times
- [ ] Verify chatbot responses

### Hàng tuần:
- [ ] Review error patterns
- [ ] Check database size
- [ ] Update dependencies nếu cần

### Hàng tháng:
- [ ] Rotate API keys
- [ ] Review and optimize queries
- [ ] Update documentation

---

## 🔒 **SECURITY CHECKLIST**

- ✅ `.env` in `.gitignore`
- ✅ `firebase_auth.json` in `.gitignore`
- ✅ API keys in Environment Variables
- ✅ Firebase credentials in Secret Files
- ✅ CORS configured
- ⚠️ Rate limiting (TODO)
- ⚠️ Input validation (TODO)
- ⚠️ SQL injection protection (TODO - using Firebase)

---

## 📞 **SUPPORT & RESOURCES**

- Render Dashboard: https://dashboard.render.com
- GitHub Repo: https://github.com/dmtriet11/backend_foodapp
- Render Docs: https://render.com/docs
- Flask Docs: https://flask.palletsprojects.com/

---

**Last Updated**: December 9, 2025
**Version**: 1.0
**Status**: Production Ready ✅
