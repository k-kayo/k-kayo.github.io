from flask import Flask, request, jsonify, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from redis import Redis
import requests
from cryptography.fernet import Fernet
from logging.handlers import RotatingFileHandler
from redis import Redis
import os
import time
import logging
from dotenv import load_dotenv

# ロガーの設定
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ログファイルの設定
handler = logging.handlers.RotatingFileHandler('app.log', maxBytes=10**6, backupCount=3) # 1MBごとにローテーション
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler) # ログハンドラーを追加

# .env ファイルの読み込み
load_dotenv()

# Flask アプリの設定
app = Flask(__name__)
redis = Redis(host='localhost', port=6379)

@app.route('/')
def hello():
    redis.incr('hits')
    return f'Hello! This page has been visited {redis.get("hits").decode("utf-8")} times.'

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)

# Redisの設定
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_connection = Redis.from_url(redis_url)
limiter = Limiter(key_func=get_remote_address, storage_uri=redis_url, app=app)

@app.route('/some_endpoint')
@limiter.limit("5 per minute")  # 1分に5回までリクエストを許可
def some_endpoint():
    return "Hello, world!"

@app.before_request
def log_request_info():
    app.logger.info('アクセスログ: %s %s', request.method, request.path)
class Config:
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    BASE_ACCESS_TOKEN = os.getenv("BASE_ACCESS_TOKEN")
    BASE_REFRESH_TOKEN = os.getenv("BASE_REFRESH_TOKEN")
    REDIRECT_URI = os.getenv("REDIRECT_URI", "http://127.0.0.1:8000/callback")
    ACCESS_TOKEN_EXPIRES_AT = float(os.getenv("ACCESS_TOKEN_EXPIRES_AT", 0))

app.config.from_object(Config)

# トークン取得URL # 認証コードを使ってアクセストークンを取得
TOKEN_URL = os.getenv("TOKEN_URL")

def update_env_file(variable_name, value):
    """指定された環境変数を.envファイルに書き込む（更新または追加）"""
    key_found = False  # key_foundを初期化
    """
    # .envファイルをUTF-8エンコーディングで読み書き # .env ファイルを読み込んで行ごとに処理
    """
    with open(".env", "r", encoding="utf-8") as file:
        lines = file.readlines()

    # .envファイル内の指定したキーを更新
    with open(".env", "w", encoding="utf-8") as file:
        for line in lines:
            if line.startswith(variable_name + "="):  # keyが含まれる行を確認
                file.write(f"{variable_name}={value}\n")  # 見つかれば更新
                key_found = True   # 更新したのでkey_foundをTrueに
            else:
                file.write(line)  # 他の行はそのまま書き込み
         # keyが見つからなかった場合、新しい行を追加
        if not key_found:
            file.write(f"{variable_name}={value}\n")

@app.route("/index")
@limiter.limit("5 per minute") # 1分に5回までアクセス可能 
def index():
    return "Welcome to the site!"

@app.route('/callback', methods=['GET'])
def callback():
    code = request.args.get('code')
    if not code:
        error_message = "認証コードが無効です。もう一度やり直してください。"
        app.logger.error(f"Error: {error_message}")
        return "Error: No code received", 400  # ユーザーにエラーメッセージを返す

    data = {
        "grant_type": "authorization_code",
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "code": code,
        "redirect_uri": os.getenv("REDIRECT_URI", "http://127.0.0.1:8000/callback"),
    }
    response = requests.post(TOKEN_URL, data=data)

    if response.status_code == 200:
        token_data = response.json()
        global BASE_ACCESS_TOKEN, BASE_REFRESH_TOKEN, ACCESS_TOKEN_EXPIRES_AT
        BASE_ACCESS_TOKEN = token_data["access_token"]
        BASE_REFRESH_TOKEN = token_data["refresh_token"]
        expires_in = token_data["expires_in"]
        ACCESS_TOKEN_EXPIRES_AT = time.time() + expires_in

        # トークンを.envに保存
        update_env_file("BASE_ACCESS_TOKEN", BASE_ACCESS_TOKEN)
        update_env_file("BASE_REFRESH_TOKEN", BASE_REFRESH_TOKEN)
        update_env_file("ACCESS_TOKEN_EXPIRES_AT", ACCESS_TOKEN_EXPIRES_AT)

        return jsonify({"access_token": BASE_ACCESS_TOKEN, "refresh_token": BASE_REFRESH_TOKEN}), 200
    else:
        return f"Error: {response.status_code} - {response.text}", 400


# アクセストークンの更新処理  ｜ check_and_refresh_access_token() 関数
def check_and_refresh_access_token():
    global BASE_ACCESS_TOKEN, ACCESS_TOKEN_EXPIRES_AT
    """
    アクセストークンの有効期限を確認し、期限切れなら更新
    """
    if time.time() >= ACCESS_TOKEN_EXPIRES_AT:
        print("アクセストークンが期限切れです。更新を行います。")
        get_new_access_token()
    else:
        print("アクセストークンは有効です。")

def get_new_access_token():
    global BASE_ACCESS_TOKEN, BASE_REFRESH_TOKEN, ACCESS_TOKEN_EXPIRES_AT
    """
    リフレッシュトークンを使用して新しいアクセストークンを取得
    """
    data = {
        "grant_type": "refresh_token",
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "refresh_token": BASE_REFRESH_TOKEN,
    }
    response = requests.post(TOKEN_URL, data=data)
    if response.status_code == 200:
        token_data = response.json()
        BASE_ACCESS_TOKEN = token_data["access_token"]
        expires_in = token_data["expires_in"]
        BASE_REFRESH_TOKEN = token_data["refresh_token"]
        ACCESS_TOKEN_EXPIRES_AT = time.time() + expires_in
        # トークンを.envに保存 # トークンを更新
        update_env_file("BASE_ACCESS_TOKEN", BASE_ACCESS_TOKEN)
        update_env_file("BASE_REFRESH_TOKEN", BASE_REFRESH_TOKEN)
        update_env_file("ACCESS_TOKEN_EXPIRES_AT", ACCESS_TOKEN_EXPIRES_AT)
        print("新しいアクセストークンを取得しました:", BASE_ACCESS_TOKEN)
    else:
        print("リフレッシュトークンが期限切れです。再認証を行います。")
        # 認証フローに戻る処理
        return redirect(url_for('authorize'))

@app.route('/authorize')
def authorize():
    """
    ユーザーに認証を求め、認証コードを取得するためのURLにリダイレクト
    """
    authorization_url = f"https://api.thebase.in/oauth/authorize?client_id={app.config['CLIENT_ID']}&redirect_uri={app.config['REDIRECT_URI']}&response_type=code"
    return redirect(authorization_url)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('app.log')
        ]
    )  # ログレベルをDEBUGに設定
    app.run(debug=True, host='0.0.0.0', port=8000) # ここでポートを8000に指定
    # ↑ 開発環境では上のコードで、本番環境では下のコード waitress を使用します：
    # なので、本番環境移行時はこの下のコメントアウトは解除すること！！
    # 本番環境用のコード（開発環境ではコメントアウト）
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=8000)
# この上のに二行は本番環境移行時にコメントアウト解除！！


# ここから下は？？
# from waitress import serve から始まる部分は、Waitress を使ってFlaskアプリを実行するためのコードです。これはFlaskの開発サーバーよりも本番環境に適しています。
# ただし、本番環境では Waitress などを使用することをお勧めします。


# ↓ Waitress などの本番環境用サーバーを使用するためのコードは、  ↓  必ずこの下すべてを  ↓  本番環境に移行する際にコメントアウトを解除すること！！！

# from waitress import serve
# from app import app

# if __name__ == "__main__":
#     serve(app, host="0.0.0.0", port=8000)

# for i in range(10000):
#     logger.info(f"ログメッセージ{i}")

# def get_key():
#     if os.path.exists('secret.key'):
#         with open('secret.key', 'rb') as key_file:
#             return key_file.read()
#     else:
#         # 新しくキーを生成
#         key = Fernet.generate_key()
#         with open('secret.key', 'wb') as key_file:
#             key_file.write(key)
#         return key

# # トークンの暗号化
# cipher_suite = Fernet(key)
# encrypted_token = cipher_suite.encrypt(b"your_token_here")

# # 環境変数に保存する例
# with open('.env', 'a') as f:
#     f.write(f"ENCRYPTED_TOKEN={encrypted_token.decode()}\n")

# # トークンを復号化
# def decrypt_token(encrypted_token):
#     key = get_key()
#     cipher_suite = Fernet(key)
#     decrypted_token = cipher.decrypt(encrypted_token).decode()
#     return decrypted_token

# # 環境変数に保存する例
# with open('.env', 'a') as f:
#     f.write(f"ENCRYPTED_TOKEN={encrypted_token.decode()}\n")

# # トークンを復号化
# cipher_suite = Fernet(key)
# decrypted_token = cipher_suite.decrypt(encrypted_token).decode()
# print(decrypted_token)

# # 復号化
# key = os.getenv("ENCRYPTION_KEY")  # .envから取得
# encrypted_token = os.getenv("ENCRYPTED_API_TOKEN")  # 暗号化されたトークン
# if not key or not encrypted_token:
#     raise ValueError("暗号化キーまたはトークンが見つかりません。")

# fernet = Fernet(key)
# token = fernet.decrypt(encrypted_token.encode()).decode()

# # トークンを使ってAPIリクエスト
# print("復号化されたトークン:", token)

# # 鍵の生成
# def generate_key():
#     key = Fernet.generate_key()
#     with open('secret.key', 'wb') as key_file:
#         key_file.write(key)
#     return key

# # トークンを暗号化
# def encrypt_token(token):
#     key = generate_key()  # 鍵を生成
#     cipher_suite = Fernet(key)
#     encrypted_token = cipher_suite.encrypt(token.encode())
#     return encrypted_token

# # トークンを復号化
# def decrypt_token(encrypted_token):
#     key = get_key()  # 生成または保存されたキーを取得
#     cipher_suite = Fernet(key)
#     decrypted_token = cipher_suite.decrypt(encrypted_token).decode()
#     return decrypted_token


# ここまでコメントアウト解除する（本番環境移行のとき）