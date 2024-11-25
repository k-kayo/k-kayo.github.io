from flask import Flask, request, jsonify, redirect, url_for
import requests
import os
import time
import logging
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

app = Flask(__name__)

# BASE APIに必要な情報  # .envファイルから取得する # 環境変数を読み込む
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
BASE_REFRESH_TOKEN = os.getenv("BASE_REFRESH_TOKEN")
BASE_ACCESS_TOKEN = os.getenv("BASE_ACCESS_TOKEN")
ACCESS_TOKEN_EXPIRES_AT = float(os.getenv("ACCESS_TOKEN_EXPIRES_AT", 0))  # 有効期限（UNIXタイム）

# トークン取得URL # 認証コードを使ってアクセストークンを取得
TOKEN_URL = "https://api.thebase.in/1/oauth/token"


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
        # key_found = False
        for line in lines:
            if line.startswith(variable_name + "="):  # keyが含まれる行を確認
                file.write(f"{variable_name}={value}\n")  # 見つかれば更新
                key_found = True   # 更新したのでkey_foundをTrueに
            else:
                file.write(line)  # 他の行はそのまま書き込み
         # keyが見つからなかった場合、新しい行を追加
        if not key_found:
            file.write(f"{variable_name}={value}\n")

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/callback', methods=['GET'])
def callback():
    """
    認証コードを受け取り、アクセストークンとリフレッシュトークンを取得する # リダイレクトURLから認証コードを取得
    """
    code = request.args.get('code')
    if not code:
        error_message = "認証コードが無効です。もう一度やり直してください。"
        app.logger.error(f"Error: {error_message}")
        return "Error: No code received", 400  # ユーザーにエラーメッセージを返す

    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": "http://127.0.0.1:8000/callback",
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
    """
    アクセストークンの有効期限を確認し、期限切れなら更新
    """
    if time.time() >= ACCESS_TOKEN_EXPIRES_AT:
        # アクセストークンが期限切れ
        print("アクセストークンが期限切れです。更新を行います。")
        get_new_access_token()
    else:
        print("アクセストークンは有効です。")

def get_new_access_token():
    """
    リフレッシュトークンを使用して新しいアクセストークンを取得
    """
    data = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": BASE_REFRESH_TOKEN,
    }

    response = requests.post(TOKEN_URL, data=data)

    if response.status_code == 200:
        token_data = response.json()
        BASE_ACCESS_TOKEN = token_data["access_token"]
        BASE_REFRESH_TOKEN = token_data["refresh_token"]
        expires_in = token_data["expires_in"]
        ACCESS_TOKEN_EXPIRES_AT = time.time() + expires_in

        # トークンを更新
        # トークンを.envに保存
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
    authorization_url = f"https://api.thebase.in/oauth/authorize?client_id={CLIENT_ID}&redirect_uri=http://127.0.0.1:8000/callback&response_type=code"
    return redirect(authorization_url)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True, port=8000)

# print("CLIENT_ID:", os.getenv("CLIENT_ID"))
# print("CLIENT_SECRET:", os.getenv("CLIENT_SECRET"))