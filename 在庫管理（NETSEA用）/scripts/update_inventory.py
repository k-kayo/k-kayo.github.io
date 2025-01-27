from flask import Flask, request, jsonify, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from redis import Redis
import requests
import csv
import os
import time
import logging
import logging.handlers
from dotenv import load_dotenv


# .env ファイルの読み込み
load_dotenv()

app = Flask(__name__)

# 環境変数
TOKEN_URL = os.getenv("TOKEN_URL")
BASE_ACCESS_TOKEN = os.getenv("BASE_ACCESS_TOKEN")
BASE_REFRESH_TOKEN = os.getenv("BASE_REFRESH_TOKEN")
BASE_API_URL = os.getenv('BASE_API_URL')
NETSEA_API_URL = os.getenv('NETSEA_API_URL')
NETSEA_ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
LOG_FILE = "sync_log.txt"  # ログファイルの名前
# ACCESS_TOKEN_EXPIRES_AT = float(os.getenv("ACCESS_TOKEN_EXPIRES_AT", 0))
ACCESS_TOKEN_EXPIRES_AT = float(os.getenv("ACCESS_TOKEN_EXPIRES_AT", "0"))

# 共通関数をここに配置
def make_api_request(url, method="GET", headers=None, json=None):
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=json)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=json)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        log_message(f"APIリクエストエラー: {e}")
        return None

# ログファイルのパスを指定
log_file_path = "logs/sync_log.txt"

# ログの設定を統一
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ログファイルの設定
handler = logging.handlers.RotatingFileHandler('app.log', maxBytes=10**6, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# ログを記録する例
def log_message(message):
    logger.info(message)

def log_message(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file_path, "a", encoding="utf-8") as
    log_file: log_file.write(f"[{timestamp}] {message}\n")

log_message("このメッセージはapp.logに記録されます。")


# # ログ記録用関数   ※削除して良いらしいが念のため、残します
# def log_message(message):
#     with open(LOG_FILE, "a") as log_file:
#         timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
#         log_file.write(f"[{timestamp}] {message}\n")
#     print(message)

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

# NETSEAのアクセストークンを取得・更新する関数
def get_new_netsea_access_token():
    data = {
        "client_id": os.getenv("NETSEA_CLIENT_ID"),
        "client_secret": os.getenv("NETSEA_CLIENT_SECRET"),
    }
    response = requests.post(os.getenv("NETSEA_TOKEN_URL"), data=data)
    log_message(f"NETSEAトークン取得APIレスポンス: {response.status_code}, {response.text}")
    if response.status_code == 200:
        token_data = response.json()
        netsea_access_token = token_data["access_token"]
        update_env_file("NETSEA_ACCESS_TOKEN", netsea_access_token)
        print("新しいNETSEAアクセストークンを取得しました:", netsea_access_token)
        return netsea_access_token
    else:
        print("NETSEAアクセストークンの取得に失敗しました。")
        log_message(f"NETSEAアクセストークンの取得に失敗しました: {response.status_code}, {response.text}")
        return None


def get_new_base_access_token():
    global BASE_ACCESS_TOKEN, BASE_REFRESH_TOKEN, ACCESS_TOKEN_EXPIRES_AT
    data = {
        "grant_type": "refresh_token",
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "refresh_token": BASE_REFRESH_TOKEN,
        # "refresh_token": os.getenv("NETSEA_REFRESH_TOKEN"),
    }
    response = requests.post(TOKEN_URL, data=data)
    # response = requests.post(os.getenv("TOKEN_URL"), data=data)
    log_message(f"BASEトークン更新APIレスポンス: {response.status_code}, {response.text}")
    if response.status_code == 200:
        token_data = response.json()
        BASE_ACCESS_TOKEN = token_data["access_token"]
        expires_in = token_data["expires_in"]
        BASE_REFRESH_TOKEN = token_data["refresh_token"]
        ACCESS_TOKEN_EXPIRES_AT = time.time() + expires_in
        update_env_file("BASE_ACCESS_TOKEN", BASE_ACCESS_TOKEN)
        update_env_file("BASE_REFRESH_TOKEN", BASE_REFRESH_TOKEN)
        update_env_file("ACCESS_TOKEN_EXPIRES_AT", ACCESS_TOKEN_EXPIRES_AT)
        print("新しいBASEアクセストークンを取得しました:", BASE_ACCESS_TOKEN)
    else:
        print("BASEリフレッシュトークンが期限切れです。再認証を行います。")
        log_message(f"BASEリフレッシュトークンの期限切れ: {response.status_code}, {response.text}")
        # 認証フローに戻る処理 ｜ 再認証の処理を追加する場合はここに記述
        # with app.app_context():
        #     return redirect(url_for('authorize'))

# BASEとNETSEAのトークンの確認と更新
def check_and_refresh_access_token():
    global BASE_ACCESS_TOKEN, ACCESS_TOKEN_EXPIRES_AT
    # global BASE_ACCESS_TOKEN, ACCESS_TOKEN_EXPIRES_AT, NETSEA_ACCESS_TOKEN
    # BASEのトークン確認と更新
    if time.time() >= ACCESS_TOKEN_EXPIRES_AT:
        print("BASEアクセストークンが期限切れです。更新を行います。")
        # get_new_access_token()
        get_new_base_access_token()
    else:
        print("BASEアクセストークンは有効です。")

    # NETSEAのトークン確認と更新
    netsea_access_token = os.getenv('NETSEA_ACCESS_TOKEN')
    # if 'NETSEA_ACCESS_TOKEN' in os.environ:
    if netsea_access_token is None:
        # if not validate_netsea_token():
        print("NETSEAアクセストークンが無効です。手動で更新してください。")
        get_new_netsea_access_token()
    else:
        print("NETSEAアクセストークンは有効です。")
    # else: print("NETSEAアクセストークンが設定されていません。")


# CSVファイルからダイレクト商品IDを取得
def load_direct_item_ids(csv_filename):
    try:
        with open(csv_filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            return [row[0] for row in reader]  # 1列目に商品IDがあると仮定
    except FileNotFoundError:
        log_message(f"CSVファイルが見つかりません: {csv_filename}")
        return []

#-------------- NETSEAの在庫情報を取得 ----------------#
# NETSEA APIから在庫情報を取得し、在庫あり/なしに応じて在庫数を設定しています。ただし、在庫数が固定値（0または10）になっています。実際の在庫数に応じて動的に設定する方が良いかもしれません。
def get_netsea_product_list(direct_item_ids):
    netsea_access_token = os.getenv('NETSEA_ACCESS_TOKEN')
    if netsea_access_token is None:
        log_message("NETSEA_ACCESS_TOKEN が設定されていません。手動でアクセストークンを更新してください")
        netsea_access_token = get_new_netsea_access_token()
        if netsea_access_token is None:
            return []
    # headers = {"Authorization": f"Bearer {NETSEA_ACCESS_TOKEN}"}
    headers = {
        # "Authorization": f"Bearer {os.getenv('NETSEA_ACCESS_TOKEN').encode('ascii', 'ignore').decode()}",
        "Authorization": f"Bearer {netsea_access_token}",
        "Content-Type": "application/json",
    }
    data = {"direct_item_ids": ','.join(direct_item_ids)}
    # response = requests.post(NETSEA_API_URL + "/items", headers=headers, data=data)
    response = requests.post(NETSEA_API_URL, headers=headers, json=data)

    if response.headers.get("Content-Type") == "application/json":
        product_list = response.json().get("data", [])
    else:
        log_message(f"NETSEA APIエラー: 無効なレスポンス形式 - {response.text}")
        return []

    if response.status_code == 401:  # 認証エラー
        log_message("NETSEA API: トークンが無効です。トークンを再取得します。")
        # get_new_netsea_access_token() # トークンを更新
        netsea_access_token = get_new_netsea_access_token() # トークンを更新する関数
        if netsea_access_token is None:
            return []
        # headers["Authorization"] = f"Bearer {NETSEA_ACCESS_TOKEN}"  # 新しいトークンを使用
        # headers["Authorization"] = f"Bearer {os.getenv('NETSEA_ACCESS_TOKEN').encode('ascii', 'ignore').decode()}" # 新しいトークンを使用
        headers["Authorization"] = f"Bearer {netsea_access_token.encode('ascii', 'ignore').decode()}" # 新しいトークンを使用
        response = requests.post(NETSEA_API_URL, headers=headers, json=data)  # 再リクエスト

    if response.status_code == 200:
        product_list = response.json().get('data', [])
        log_message(f"NETSEA APIレスポンス: {response.json()}")
        # return response.json().get('data', [])
        return product_list
    else:
        log_message(f"NETSEA APIエラー: 商品一覧の取得に失敗しました - {response.status_code}, {response.text}")
        return []

def get_set_num(direct_item_id):
    product_list = get_netsea_product_list([direct_item_id])
    if product_list:
        item_info = product_list[0]
        set_num = item_info['set'][0]['set_num'] if 'set' in item_info and item_info['set'] else 0
        return set_num
    else:
        log_message(f"商品ID {direct_item_id} の情報が見つかりませんでした。")
        return 0

#----------------- BASEの商品在庫を更新 -----------------#
# BASEの在庫を更新するための関数です。APIのエンドポイントURLが正しくフォーマットされていることを確認します。
def update_base_stock(product_id, stock_status):
    headers = {
        "Authorization": f"Bearer {BASE_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {"product": {"stock": stock_status}}
    try:
        response = requests.put(BASE_API_URL.format(product_id=product_id), json=data, headers=headers)
        if response.status_code == 200:
            log_message(f"BASE在庫更新成功: 商品ID {product_id} - 在庫 {stock_status}")
        else:
            log_message(f"BASE在庫更新失敗: 商品ID {product_id} - {response.status_code}, {response.text}")
    except requests.RequestException as e:
        log_message(f"BASE APIリクエスト失敗: {e}")

#-------------------- 在庫同期のメイン処理 ------------------------#
# CSVファイルから商品IDを取得し、各商品についてNETSEAの在庫を確認して、BASEの在庫を更新するメイン処理です。
def sync_inventory(csv_filename):
    log_message("在庫同期を開始します...")

    # トークンの確認と更新
    check_and_refresh_access_token()

    # CSVファイルからダイレクト商品IDを取得
    direct_item_ids = load_direct_item_ids(csv_filename)

    if not direct_item_ids:
        log_message("CSVファイルから商品IDが読み込めませんでした。同期を中止します。")
        return

    # 各商品について在庫情報を取得してBASEの在庫を更新
    for direct_item_id in direct_item_ids:
        set_num = get_set_num(direct_item_id) # 商品のバリエーション在庫数を取得
        if set_num > 0:
            base_product_id = direct_item_id # 商品IDが同じであると仮定
            update_base_stock(base_product_id, set_num)
        else:
            # log_message(f"在庫情報の取得に失敗しました。商品ID {direct_item_id}")
            log_message(f"商品ID {direct_item_id} の在庫情報取得に失敗しました。")

    # 在庫同期処理をここに追加
    log_message("在庫同期が完了しました。")

# スクリプトを実行する
if __name__ == "__main__":
    with app.app_context():
        sync_inventory("itemdata_4 のコピー.csv")

