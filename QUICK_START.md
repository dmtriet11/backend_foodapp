# ⚡ QUICK START - RENDER DEPLOYMENT

**5 bước nhanh để deploy lên Render:**

## 1️⃣ Push Code lên GitHub ✅
```bash
cd d:\24C02\CompThinking\backend_deploy\backend_foodapp
git push origin main
```

## 2️⃣ Tạo Service trên Render
1. Vào https://dashboard.render.com
2. **New +** → **Web Service**
3. Connect repo: `dmtriet11/backend_foodapp`
4. Settings:
   - **Name:** backend-foodapp
   - **Region:** Singapore
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn App:app`
   - **Plan:** Free

## 3️⃣ Thêm Environment Variables
Vào tab **Environment** → Add 6 biến:

```env
GOOGLE_API_KEY=your_google_maps_api_key
FIREBASE_DB_URL=https://food-app-d0127-default-rtdb.firebaseio.com
OPENAI_API_KEY=your_openai_api_key
SENDER_EMAIL=your_email@gmail.com
SENDER_APP_PASSWORD=your_gmail_app_password
FLASK_ENV=production
```

## 4️⃣ Upload Firebase Credentials
Vào tab **Environment** → **Secret Files** → Add:

```
Filename: /etc/secrets/firebase_auth.json
Contents: [Paste nội dung file firebase_auth.json]
```

**Lấy nội dung:**
```powershell
Get-Content d:\24C02\CompThinking\backend_deploy\backend_foodapp\firebase_auth.json | clip
```
Sau đó Ctrl+V vào ô Contents

## 5️⃣ Deploy!
Click **"Create Web Service"** → Đợi deploy xong (~2-3 phút)

---

## ✅ Verify Deployment

**Production URL:** https://backend-foodapp-1-wr4a.onrender.com

Test ngay:
```bash
cd backend_foodapp
python test_api_comprehensive.py
```

Kết quả mong đợi: **90%+ tests passed**

---

## 🔄 Auto-Deploy Setup

Sau khi deploy lần đầu, mỗi lần push code:
```bash
git add .
git commit -m "Update feature"
git push origin main
```
→ Render tự động deploy! ✨

---

## 📖 Chi tiết đầy đủ
Xem file: **[RENDER_DEPLOYMENT_GUIDE.md](RENDER_DEPLOYMENT_GUIDE.md)**

## 🧪 Test Suite
- **API Endpoints:** `python test_api_comprehensive.py`
- **Authentication:** `python test_auth_endpoints.py`

## 🔧 Troubleshooting
**Service không start:** Check Logs tab trên Render  
**Firebase error:** Verify Secret File đã upload đúng  
**API key error:** Check Environment Variables đủ 6 biến  

---

**Status:** 🟢 Production Ready | **Endpoints:** 37 total | **Coverage:** 90.9%
