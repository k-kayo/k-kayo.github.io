from flask import Flask, request, jsonify, redirect, url_for
import requests
import os
import time
from dotenv import load_dotenv
from datetime import datetime, timedelta

# .envファイルから環境変数を読み込む
load_dotenv()

app = Flask(__name__)

# BASE APIに必要な情報
BASE_CLIENT_ID = os.getenv("BASE_CLIENT_ID")
BASE_CLIENT_SECRET  = os.getenv('BASE_CLIENT_SECRET')
BASE_REFRESH_TOKEN = os.getenv("BASE_REFRESH_TOKEN")
BASE_ACCESS_TOKEN = os.getenv("BASE_ACCESS_TOKEN")
ACCESS_TOKEN_EXPIRES_AT = float(os.getenv("ACCESS_TOKEN_EXPIRES_AT", 0))  # 有効期限（UNIXタイム）

# トークン取得URL
TOKEN_URL = "https://api.thebase.in/1/oauth/token"

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/callback', methods=['GET'])
def callback():
     """
    認証コードを受け取り、アクセストークンとリフレッシュトークンを取得する
    """
code = request.args.get('code')
if not code:
        return "Error: No code received", 400
# 認証コードを使ってアクセストークンを取得
response = requests.post(TOKEN_URL, data=data)

if response.status_code == 200:
    token_data = response.json()
    BASE_ACCESS_TOKEN = token_data["access_token"]
    BASE_REFRESH_TOKEN = token_data["refresh_token"]
    expires_in = token_data["expires_in"]
    ACCESS_TOKEN_EXPIRES_AT = time.time() + expires_in

    # トークンを保存する処理
    with open(".env", "a") as env_file:
        env_file.write(f"\nBASE_ACCESS_TOKEN={BASE_ACCESS_TOKEN}")
        env_file.write(f"\nBASE_REFRESH_TOKEN={BASE_REFRESH_TOKEN}")
        env_file.write(f"\nACCESS_TOKEN_EXPIRES_AT={ACCESS_TOKEN_EXPIRES_AT}")


def get_new_access_token():
    """
    リフレッシュトークンを使用して新しいアクセストークンを取得
    """
    global BASE_ACCESS_TOKEN, BASE_REFRESH_TOKEN, ACCESS_TOKEN_EXPIRES_AT

    data = {
        "grant_type": "refresh_token",  # リフレッシュトークンで新しいアクセストークンを取得
        "base_client_id": BASE_CLIENT_SECRET,  # BASEで登録したクライアントID
        "base_client_secret": BASE_CLIENT_SECRET,  # BASEで登録したクライアントシークレット
        "refresh_token": BASE_REFRESH_TOKEN,      # .envファイルから取得したrefresh_token
        "redirect_uri": "http://127.0.0.1:8000/callback",  # 登録したリダイレクトURI
    }

    # この行のインデントを揃える
    response = requests.post(TOKEN_URL, data=data)

    # レスポンスが成功の場合
    if response.status_code == 200:
        token_data = response.json()
        BASE_ACCESS_TOKEN = token_data["base_access_token"]
        BASE_REFRESH_TOKEN = token_data["base_refresh_token"]  # 新しいリフレッシュトークン
        expires_in = token_data["expires_in"]
        ACCESS_TOKEN_EXPIRES_AT = time.time() + expires_in  # 有効期限を更新

            # トークンを保存
        with open(".env", "a") as env_file:
            env_file.write(f"\nBASE_ACCESS_TOKEN={BASE_ACCESS_TOKEN}")
            env_file.write(f"\nBASE_REFRESH_TOKEN={BASE_REFRESH_TOKEN}")
            env_file.write(f"\nACCESS_TOKEN_EXPIRES_AT={ACCESS_TOKEN_EXPIRES_AT}")

        return jsonify({"access_token": BASE_ACCESS_TOKEN, "refresh_token": BASE_REFRESH_TOKEN}), 200
    else:
        return f"Error: {response.status_code} - {response.text}", 400

        print("新しいアクセストークンを取得しました:", BASE_ACCESS_TOKEN)
    else:
        print("リフレッシュトークンが期限切れです。再認証を行います。")
        return redirect(url_for('authorize'))  # 再認証を行うためのルートにリダイレクト

def check_and_refresh_access_token():
    """
    アクセストークンの有効期限を確認し、期限切れなら更新
    """
    print(f"現在時刻: {time.time()}, 有効期限: {ACCESS_TOKEN_EXPIRES_AT}")
    if time.time() >= ACCESS_TOKEN_EXPIRES_AT:
        print("アクセストークンが期限切れです。更新を行います。")
        get_new_access_token()
    else:
        print("アクセストークンは有効です。")

# 認証用のエンドポイント
@app.route('/authorize')
def authorize():
    """
    ユーザーに認証を求め、認証コードを取得するためのURLにリダイレクト
    """
    authorization_url = f"https://api.thebase.in/oauth/authorize?base_client_id={BASE_CLIENT_ID}&redirect_uri=http://127.0.0.1:8000/callback&response_type=code"
    return redirect(authorization_url)



# APIリクエストで使用する際のヘッダー
headers = {
    "Authorization": f"Bearer {BASE_ACCESS_TOKEN}"
}

# デバッグモードを有効にする
app.debug = True



if __name__ == "__main__":
    app.run(debug=True, port=8000)