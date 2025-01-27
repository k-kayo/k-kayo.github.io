import os
import json
import time
from dotenv import load_dotenv
from datetime import datetime

# 環境変数の読み込み
load_dotenv()

# トークンの発行日時（例）
BASE_ACCESS_TOKEN_ISSUED_AT = float(os.getenv("BASE_ACCESS_TOKEN_ISSUED_AT", 0))
NETSEA_ACCESS_TOKEN_ISSUED_AT = float(os.getenv("NETSEA_ACCESS_TOKEN_ISSUED_AT", 0))

# 有効期限（秒）
BASE_EXPIRATION_PERIOD = 30 * 24 * 60 * 60  # 30日間の有効期限
NETSEA_EXPIRATION_PERIOD = 180 * 24 * 60 * 60  # 180日間の有効期限

# 現在時刻
current_time = time.time()
# アクセストークンの有効期限（例: 1時間=3600秒
expires_in = 3600 # 実際の期限に変更
# 有効期限のエポックタイムスタンプ
access_token_expires_at = current_time + expires_in

# .envファイルの更新
def update_env_file(variable_name, value):
    key_found = False
    with open(".env", "r", encoding="utf-8") as file:
        lines = file.readlines()

    with open(".env", "w", encoding="utf-8") as file:
        for line in lines:
            if line.startswith(variable_name + "="):
                file.write(f"{variable_name}={value}\n")
                key_found = True
            else:
                file.write(line)
        if not key_found:
            file.write(f"{variable_name}={value}\n")

update_env_file("ACCESS_TOKEN_EXPIRES_AT", access_token_expires_at)

print(f"アクセストークンの有効期限を設定しました: {access_token_expires_at}")

# BASEの有効期限の計算
base_expiration_time = BASE_ACCESS_TOKEN_ISSUED_AT + BASE_EXPIRATION_PERIOD

# NETSEAの有効期限の計算
netsea_expiration_time = NETSEA_ACCESS_TOKEN_ISSUED_AT + NETSEA_EXPIRATION_PERIOD

# BASEトークンの有効期限切れの確認
if current_time >= base_expiration_time:
    print("BASEトークンの有効期限が切れています。")
else:
    remaining_days = (base_expiration_time - current_time) / (24 * 60 * 60)
    print(f"BASEトークンは有効です。残り{remaining_days:.2f}日間有効です。")

# NETSEAトークンの有効期限切れの確認
if current_time >= netsea_expiration_time:
    print("NETSEAトークンの有効期限が切れています。")
else:
    remaining_days = (netsea_expiration_time - current_time) / (24 * 60 * 60)
    print(f"NETSEAトークンは有効です。残り{remaining_days:.2f}日間有効です。")


# ここから上は元のコード




# ここから下はすべて12/3に作成したコード

# # JSONファイルからトークン情報を読み込む
# def load_access_token():
#     try:
#         with open("access_token.json", "r", encoding="utf-8") as file:
#             return json.load(file)
#     except FileNotFoundError:
#         return None

# # トークンの有効期限確認
# def check_token_expiry():
#     token_data = load_access_token()
#     if token_data is None:
#         print("トークン情報が見つかりません。")
#         return

#     current_time = time.time()
#     expires_at = token_data["expires_at"]

#     if current_time >= expires_at:
#         print("トークンの有効期限が切れています。新しいトークンを生成する必要があります。")
#         # 新しいトークンを生成する処理をここに追加
#         # 例: save_access_token()を呼び出して、新しいトークンを保存する
#     else:
#         remaining_time = expires_at - current_time
#         print(f"トークンは有効です。残り時間: {remaining_time:.2f}秒")

# check_token_expiry()

