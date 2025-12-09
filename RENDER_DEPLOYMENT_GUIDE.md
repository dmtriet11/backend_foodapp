# 🚀 HƯỚNG DẪN DEPLOY FOOD APP BACKEND LÊN RENDER

**Thời gian:** ~10-15 phút  
**Yêu cầu:** Tài khoản GitHub và Render (miễn phí)

---

## 📋 BƯỚC 1: CHUẨN BỊ CODE (ĐÃ HOÀN TẤT ✅)

File cần thiết đã có sẵn:
- ✅ `Procfile` - Câu lệnh start server
- ✅ `runtime.txt` - Python version
- ✅ `requirements.txt` - Dependencies
- ✅ `App.py` - Main application với production config
- ✅ `.gitignore` - Bảo vệ secrets

---

## 📋 BƯỚC 2: PUSH CODE LÊN GITHUB

```bash
cd d:\24C02\CompThinking\backend_deploy\backend_foodapp

# Check status
git status

# Nếu có thay đổi chưa commit:
git add -A
git commit -m "Ready for production deployment"
git push origin main
```

**Verify:** Vào https://github.com/dmtriet11/backend_foodapp và check code đã lên chưa

---

## 📋 BƯỚC 3: TẠO WEB SERVICE TRÊN RENDER

### 3.1. Đăng nhập Render
1. Vào https://dashboard.render.com
2. Đăng nhập bằng GitHub account
3. Cho phép Render truy cập repository

### 3.2. Tạo New Web Service
1. Click **"New +"** → **"Web Service"**
2. Chọn repository: **`dmtriet11/backend_foodapp`**
3. Click **"Connect"**

### 3.3. Cấu hình Service
Điền thông tin:

| Field | Value |
|-------|-------|
| **Name** | `backend-foodapp` (hoặc tên bạn muốn) |
| **Region** | Singapore (gần VN nhất) |
| **Branch** | `main` |
| **Root Directory** | để trống |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn App:app` |
| **Plan** | Free |

4. Click **"Create Web Service"** (chưa deploy ngay)

---

## 📋 BƯỚC 4: CẤU HÌNH ENVIRONMENT VARIABLES

Trước khi deploy, cần thêm các biến môi trường:

### 4.1. Vào Tab Environment
1. Trong service vừa tạo, click tab **"Environment"**
2. Tìm phần **"Environment Variables"**
3. Click **"Add Environment Variable"**

### 4.2. Thêm từng biến sau:

#### Variable 1: GOOGLE_API_KEY
```
Key: GOOGLE_API_KEY
Value: [YOUR_GOOGLE_MAPS_API_KEY]
```
👉 **Lấy ở đâu:** Google Cloud Console → APIs & Services → Credentials

#### Variable 2: FIREBASE_DB_URL
```
Key: FIREBASE_DB_URL
Value: https://food-app-d0127-default-rtdb.firebaseio.com
```
👉 **Lấy ở đâu:** Firebase Console → Realtime Database → URL

#### Variable 3: OPENAI_API_KEY
```
Key: OPENAI_API_KEY
Value: [YOUR_OPENAI_API_KEY]
```
👉 **Lấy ở đâu:** https://platform.openai.com/api-keys

#### Variable 4: SENDER_EMAIL
```
Key: SENDER_EMAIL
Value: [YOUR_EMAIL@gmail.com]
```
👉 **Dùng cho:** Gửi email xác thực

#### Variable 5: SENDER_APP_PASSWORD
```
Key: SENDER_APP_PASSWORD
Value: [YOUR_GMAIL_APP_PASSWORD]
```
👉 **Lấy ở đâu:** 
- Gmail → Cài đặt → Bảo mật
- Xác minh 2 bước (phải bật)
- Mật khẩu ứng dụng → Tạo mới

#### Variable 6: FLASK_ENV
```
Key: FLASK_ENV
Value: production
```
👉 **Mục đích:** Tắt debug mode

### 4.3. Lưu Environment Variables
Click **"Save Changes"** sau khi thêm tất cả

---

## 📋 BƯỚC 5: THÊM FIREBASE CREDENTIALS (SECRET FILE)

⚠️ **QUAN TRỌNG:** File `firebase_auth.json` KHÔNG được commit lên Git!

### 5.1. Vào Secret Files
1. Vẫn trong tab **"Environment"**
2. Scroll xuống phần **"Secret Files"**
3. Click **"Add Secret File"**

### 5.2. Thêm Firebase Credentials
```
Filename: /etc/secrets/firebase_auth.json
Contents: [Paste toàn bộ nội dung file firebase_auth.json của bạn]
```

**Cách lấy nội dung:**
```bash
# Trên Windows PowerShell:
Get-Content d:\24C02\CompThinking\backend_deploy\backend_foodapp\firebase_auth.json | clip
```
Paste vào ô "Contents"

### 5.3. Lưu Secret File
Click **"Save Changes"**

---

## 📋 BƯỚC 6: UPDATE CODE ĐỌC FIREBASE CREDENTIALS

Render lưu secret file ở `/etc/secrets/`, cần update code:

### 6.1. Mở file `core/auth_service.py`
Tìm dòng:
```python
KEY_PATH = os.path.join(BASE_DIR, "firebase_auth.json")
```

### 6.2. Thay bằng:
```python
# Check Render secret file path first, fallback to local
KEY_PATH = os.getenv('FIREBASE_KEY_PATH', '/etc/secrets/firebase_auth.json')
if not os.path.exists(KEY_PATH):
    KEY_PATH = os.path.join(BASE_DIR, "firebase_auth.json")
```

### 6.3. Commit và push:
```bash
git add core/auth_service.py
git commit -m "Support Render secret file path for Firebase credentials"
git push origin main
```

---

## 📋 BƯỚC 7: DEPLOY!

### 7.1. Trigger Deploy
Sau khi push code, Render sẽ tự động deploy.

Hoặc manual deploy:
1. Vào Render Dashboard
2. Chọn service `backend-foodapp`
3. Click tab **"Manual Deploy"** → **"Deploy latest commit"**

### 7.2. Theo dõi Build Logs
1. Click tab **"Logs"**
2. Xem quá trình build và deploy
3. Chờ đến khi thấy:
```
✔️ KHỞI TẠO FIREBASE THÀNH CÔNG!
ĐÃ TẢI restaurants.json (1458) phần tử
✅ API key loaded successfully
```

### 7.3. Lấy Production URL
Sau khi deploy xong, Render sẽ cung cấp URL:
```
https://backend-foodapp-[random].onrender.com
```

---

## 📋 BƯỚC 8: VERIFY DEPLOYMENT

### 8.1. Test Root Endpoint
```bash
# PowerShell
Invoke-WebRequest -Uri "https://YOUR-APP.onrender.com/" | Select-Object StatusCode, Content
```

Kết quả mong đợi:
```json
{
  "status": "running",
  "message": "🍜 Food App Backend API",
  "version": "1.0"
}
```

### 8.2. Chạy Comprehensive Test Suite
```bash
cd d:\24C02\CompThinking\backend_deploy\backend_foodapp

# Update BASE_URL trong test_api_comprehensive.py:
# BASE_URL = "https://YOUR-APP.onrender.com/api"

python test_api_comprehensive.py
```

### 8.3. Test Authentication Endpoints
```bash
python test_auth_endpoints.py
```

---

## 📋 BƯỚC 9: CẤU HÌNH AUTO-DEPLOY

Render đã tự động setup auto-deploy từ GitHub!

**Kiểm tra:**
1. Vào tab **"Settings"**
2. Phần **"Build & Deploy"**
3. Check **"Auto-Deploy"** = `Yes`

**Cách hoạt động:**
- Mỗi lần `git push origin main` → Render tự động deploy
- Không cần làm gì thêm!

---

## 🎯 CHECKLIST HOÀN THÀNH

Copy checklist này và tick ✅ khi hoàn thành:

### Pre-deployment
- [ ] Code đã push lên GitHub
- [ ] File `firebase_auth.json` KHÔNG bị commit (check `.gitignore`)
- [ ] Đã có các API keys: Google Maps, OpenAI, Firebase

### Render Configuration
- [ ] Tạo Web Service trên Render
- [ ] Connect với GitHub repository
- [ ] Cấu hình Build & Start command

### Environment Variables (6 biến)
- [ ] `GOOGLE_API_KEY` - Google Maps API
- [ ] `FIREBASE_DB_URL` - Firebase Realtime Database URL
- [ ] `OPENAI_API_KEY` - OpenAI API key
- [ ] `SENDER_EMAIL` - Gmail để gửi email
- [ ] `SENDER_APP_PASSWORD` - Gmail app password
- [ ] `FLASK_ENV=production` - Production mode

### Secret Files
- [ ] Upload `firebase_auth.json` vào `/etc/secrets/firebase_auth.json`

### Code Updates
- [ ] Update `core/auth_service.py` để đọc `/etc/secrets/firebase_auth.json`
- [ ] Push code update lên GitHub

### Deployment
- [ ] Trigger manual deploy hoặc đợi auto-deploy
- [ ] Check logs không có error
- [ ] Firebase initialization thành công
- [ ] Data loaded (1458 restaurants)

### Testing
- [ ] Test root endpoint `/`
- [ ] Test `/api/restaurants` (1458 records)
- [ ] Test `/api/foods` (7 records)
- [ ] Test `/api/chat` (chatbot)
- [ ] Run `test_api_comprehensive.py` (90%+ pass)
- [ ] Run `test_auth_endpoints.py`

### Final
- [ ] Lưu Production URL
- [ ] Update frontend với API URL mới
- [ ] Monitor logs trong 24h đầu

---

## 🔧 TROUBLESHOOTING

### Lỗi 1: "Module not found"
**Nguyên nhân:** Thiếu package trong `requirements.txt`

**Fix:**
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push origin main
```

### Lỗi 2: "Firebase initialization failed"
**Nguyên nhân:** Chưa upload `firebase_auth.json` hoặc sai path

**Fix:**
1. Check Secret Files có file `/etc/secrets/firebase_auth.json`
2. Check `core/auth_service.py` đọc đúng path
3. Redeploy

### Lỗi 3: "API key không được cấu hình đúng"
**Nguyên nhân:** Thiếu environment variable

**Fix:**
1. Vào Environment Variables
2. Check có đủ 6 biến
3. Click "Save Changes"
4. Redeploy

### Lỗi 4: Cold Start (~30-50s)
**Nguyên nhân:** Free tier của Render sleep sau 15 phút không dùng

**Giải pháp:**
- Request đầu tiên sẽ chậm (bình thường)
- Hoặc upgrade lên Paid plan ($7/tháng)

### Lỗi 5: Register/Login không work
**Nguyên nhân:** 
- Chưa có `firebase_auth.json`
- Email service chưa setup

**Fix:**
1. Check Secret Files có Firebase credentials
2. Check SENDER_EMAIL và SENDER_APP_PASSWORD
3. Check Gmail "Less secure app access" hoặc dùng App Password

---

## 📊 EXPECTED ENDPOINTS STATUS

Sau khi deploy xong, các endpoint này phải hoạt động:

### ✅ Working (10/11 = 90.9%)
1. `GET /` - API info
2. `GET /api/restaurants` - 1,458 restaurants
3. `POST /api/search` - Location search
4. `POST /api/restaurants/details-by-ids` - Batch fetch
5. `GET /api/foods` - 7 menu items
6. `GET /api/foods/<int:id>` - Food detail
7. `GET /api/categories` - 5 categories
8. `POST /api/map/filter` - Map filtering
9. `POST /api/chat` - Chatbot (GPT)
10. `GET /api/chat/status` - Chatbot status

### ⚠️ Known Issues
- `GET /api/restaurants/<place_id>` - 404 (dùng `/restaurants/details-by-ids` thay thế)

### 🔐 Authentication (Cần test sau khi deploy)
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `GET /api/profile` - User profile (requires token)
- `POST /api/verify` - Email verification
- `POST /api/forgot-password` - Password reset
- `POST /api/google-login` - Google OAuth

---

## 🎉 DEPLOY THÀNH CÔNG!

Sau khi hoàn thành tất cả bước trên:

**Production URL:** `https://backend-foodapp-1-wr4a.onrender.com`

**Next Steps:**
1. Cập nhật frontend với API URL mới
2. Test toàn bộ features trên production
3. Monitor logs trong vài ngày đầu
4. Setup error tracking (Sentry - optional)
5. Consider upgrade lên Paid plan nếu cần (no cold start)

**Auto-Deploy Setup:**
```bash
# Mỗi lần update code:
git add .
git commit -m "Update feature X"
git push origin main

# → Render tự động deploy! ✅
```

---

## 📞 SUPPORT

**Render Docs:** https://render.com/docs  
**GitHub Repo:** https://github.com/dmtriet11/backend_foodapp  
**Test Suite:** `python test_api_comprehensive.py`

**Render Dashboard:** https://dashboard.render.com  
**Logs:** Dashboard → Service → Logs tab  
**Restart:** Dashboard → Service → Manual Deploy → "Clear build cache & deploy"
