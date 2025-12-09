from email.mime.text import MIMEText
import random
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, auth, db
import smtplib
import json
from flask import request # ⭐️ BỔ SUNG: Import request để sử dụng trong hàm mới ⭐️

# Tải các biến môi trường
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")
USERS_PATH = os.path.join(BASE_DIR, "data", "users.json")

# Firebase credentials path - check Render secret file first, fallback to local
KEY_PATH = os.getenv('FIREBASE_KEY_PATH', '/etc/secrets/firebase_auth.json')
if not os.path.exists(KEY_PATH):
    KEY_PATH = os.path.join(BASE_DIR, "firebase_auth.json")
print(f"🔑 Firebase key path: {KEY_PATH}")

print(f"📁 Loading env from: {ENV_PATH}")
load_dotenv(ENV_PATH)

# Lấy biến môi trường
API_KEY = os.getenv('GOOGLE_API_KEY')
DB_URL = os.getenv('FIREBASE_DB_URL')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_APP_PASSWORD = os.getenv('SENDER_APP_PASSWORD')

# CLIENT_ID của t trên Google Cloud
CLIENT_ID = "656361181569-n6ec9pgtupmk4go4k22qmukrfu2gid8g.apps.googleusercontent.com"

# Khởi tạo Firebase
try:
    cred = credentials.Certificate(KEY_PATH)
    firebase_admin.initialize_app(cred, {
        'databaseURL': DB_URL
    })
    print("✔️ KHỞI TẠO FIREBASE THÀNH CÔNG!")
except FileNotFoundError:
    print(f":x: LỖI: Không tìm thấy file key Firebase tại: {KEY_PATH}")
except Exception as e:
    print(f":x: LỖI KHỞI TẠO FIREBASE: {e}")

# Hàm gửi email
def send_verification_email(to_email, code):
    try:
        print(f":incoming_envelope: Đang gửi mã xác thực tới {to_email}...")
        msg = MIMEText(f"Mã xác thực của bạn là: {code}")
        msg["Subject"] = "Xác thực tài khoản Food App"
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email

        print(f"SENDER_EMAIL={SENDER_EMAIL}")
        print(f"SENDER_APP_PASSWORD={'*' * len(SENDER_APP_PASSWORD) if SENDER_APP_PASSWORD else None}")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
            server.send_message(msg)
            print(f":white_check_mark: Đã gửi email xác thực tới {to_email}")
    except Exception as e:
        print(f":x: Lỗi khi gửi email: {e}")

# Hàm load thông tin user
def load_users():
    if not os.path.exists(USERS_PATH):
        return {}
    with open(USERS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

# ⭐️ HÀM MỚI: Lấy UID từ Header Authorization ⭐️
def get_uid_from_auth_header():
    """Lấy và xác thực Firebase ID Token từ Header Authorization, trả về UID."""
    
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise ValueError("Missing Authorization header")

    # Format phải là "Bearer <token>"
    try:
        id_token = auth_header.split(' ')[1]
    except IndexError:
        raise ValueError("Invalid Authorization header format")

    try:
        # Xác thực token bằng Firebase Admin SDK
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        return uid
    except Exception as e:
        # Token hết hạn hoặc không hợp lệ
        print(f":x: Token verification failed: {e}")
        raise ValueError("Invalid or expired token")