import requests
import csv
import os
import time
from dotenv import load_dotenv

# .env ファイルの読み込み
load_dotenv()

# 環境変数
NETSEA_ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
BASE_ACCESS_TOKEN = os.getenv("BASE_ACCESS_TOKEN")
BASE_API_URL = "https://api.thebase.in/v1/products/{product_id}"
NETSEA_API_URL = "https://api.netsea.jp/buyer/v1/items/stock"
LOG_FILE = "sync_log.txt"  # ログファイルの名前

# ログ記録用関数
def log_message(message):
    with open(LOG_FILE, "a") as log_file:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {message}\n")
    print(message)

# CSVファイルからダイレクト商品IDを取得
def load_direct_item_ids(csv_filename):
    with open(csv_filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        return [row[0] for row in reader]  # A列の値（ダイレクト商品ID）をリストで返す

# NETSEAの在庫情報を取得
def get_netsea_stock(direct_item_id):
    headers = {"Authorization": f"Bearer {NETSEA_ACCESS_TOKEN}"}
    params = {"direct_item_id": direct_item_id}
    response = requests.get(NETSEA_API_URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        sold_out_flg = data.get("sold_out_flg")
        return 0 if sold_out_flg == "Y" else 10  # 売り切れなら0、在庫ありなら10
    else:
        log_message(f"NETSEA APIエラー: 商品ID {direct_item_id} - {response.status_code}, {response.text}")
        return None

# BASEの商品在庫を更新
def update_base_stock(product_id, stock_status):
    headers = {
        "Authorization": f"Bearer {BASE_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {"product": {"stock": stock_status}}
    response = requests.put(BASE_API_URL.format(product_id=product_id), json=data, headers=headers)

    if response.status_code == 200:
        log_message(f"BASE在庫更新成功: 商品ID {product_id} - 在庫 {stock_status}")
    else:
        log_message(f"BASE在庫更新失敗: 商品ID {product_id} - {response.status_code}, {response.text}")

# メイン処理
def sync_inventory(csv_filename):
    log_message("在庫同期を開始します...")
    direct_item_ids = load_direct_item_ids(csv_filename)

    for direct_item_id in direct_item_ids:
        stock_status = get_netsea_stock(direct_item_id)

        if stock_status is not None:
            # BASEの商品IDは直接取得する仕組みが必要
            base_product_id = direct_item_id  # 仮に商品IDが同じと想定
            update_base_stock(base_product_id, stock_status)

    log_message("在庫同期が完了しました。")

# 実行
if __name__ == "__main__":
    sync_inventory("itemdata_4 のコピー.csv")
