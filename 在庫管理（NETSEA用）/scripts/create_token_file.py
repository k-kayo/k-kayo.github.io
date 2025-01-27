import json
import time
from datetime import datetime

# トークンデータを生成
token_data = {
    "access_token": "c6941a1509d059dfd2a001335984794b",
    "refresh_token": "ea6f21b00f83488cd8c7bf3c49ecc081",
    "expires_at": time.time() + 3600  # 1時間後を有効期限として設定
}

# JSONファイルに保存
def save_access_token(token_data):
    with open("access_token.json", "w", encoding="utf-8") as file:
        json.dump(token_data, file, indent=4)
        print("トークン情報が保存されました。")

save_access_token(token_data)
