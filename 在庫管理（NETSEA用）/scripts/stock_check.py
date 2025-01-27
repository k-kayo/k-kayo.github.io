from flask import Flask, redirect, url_for
import requests
import csv
import os
from dotenv import load_dotenv
import schedule
import time

# .envファイルから環境変数を読み込むload_dotenv()

headers = {"Content-Type": "application/json; charset=utf-8"}
data = {"key": "値".encode('utf-8')}


# 【環境変数の設定】
NETSEA_ACCESS_TOKEN = os.getenv("NETSEA_ACCESS_TOKEN")  # NETSEAのアクセストークン
BASE_ACCESS_TOKEN = os.getenv("BASE_ACCESS_TOKEN")  # BASEのアクセストークン
BASE_REFRESH_TOKEN = os.getenv("BASE_REFRESH_TOKEN") # BASEリフレッシュトークン
CLIENT_ID = os.getenv("CLIENT_ID") # BASEクライアントID
CLIENT_SECRET = os.getenv("CLIENT_SECRET") # BASEクライアントシークレット
# TOKEN_URL = "https://api.thebase.in/1/oauth/token"  # BASEのトークン更新用URL
TOKEN_URL = os.getenv("TOKEN_URL")
BASE_API_URL = os.getenv('BASE_API_URL') # BASE APIのベースURL｜BASEの在庫更新用エンドポイン
NETSEA_API_URL = os.getenv('NETSEA_API_URL') # NETSEA APIリクエスト

BASE_PRODUCTS_URL = f"{BASE_API_URL}/products" # 商品情報取得URL
ACCESS_TOKEN_EXPIRES_AT = float(os.getenv("ACCESS_TOKEN_EXPIRES_AT", 0)) # BASEアクセストークンの有効期限（UNIXタイム）
BASE_UPDATE_PRODUCT_URL = f"{BASE_API_URL}/products/{{identifier}}" # 商品在庫更新URL

# NETSEA APIのエンドポイントURL (NETSEA)
# url = "https://api.netsea.jp/buyer/v1/items/stock"


# Headersの分割管理
netsea_headers = {"Authorization": f"Bearer {NETSEA_ACCESS_TOKEN}"} # NETSEAヘッダー設定
# base_headers = {"Authorization": f"Bearer {BASE_ACCESS_TOKEN}"} # BASEヘッダー設定
base_headers = { 
    "Authorization": f"Bearer {BASE_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}




#-------- ここからはトークン情報と認証情報の確認と更新・取得  ------#

# アクセストークンの確認と更新｜アクセストークンの有効期限チェック
def check_and_refresh_access_token():
    global BASE_ACCESS_TOKEN, ACCESS_TOKEN_EXPIRES_AT
    "アクセストークンの有効期限を確認し、期限切れなら更新"
    if time.time() >= ACCESS_TOKEN_EXPIRES_AT:
        print("アクセストークンが期限切れです。更新を行います。")
        get_new_access_token()
    else:
        print("アクセストークンは有効です。")

# 新しいアクセストークンの取得
def get_new_access_token():
    global BASE_ACCESS_TOKEN, BASE_REFRESH_TOKEN, ACCESS_TOKEN_EXPIRES_AT
   # リフレッシュトークンを使って新しいアクセストークンを取得する処理
    url = f"{BASE_API_URL}/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": BASE_REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        token_data = response.json()
        BASE_ACCESS_TOKEN = token_data["access_token"]
        expires_in = token_data["expires_in"]
        ACCESS_TOKEN_EXPIRES_AT = time.time() + expires_in
        # ACCESS_TOKEN_EXPIRES_AT = time.time() + token_data["expires_in"]
        update_env_file("BASE_ACCESS_TOKEN", BASE_ACCESS_TOKEN) # トークンを.envに保存
        # update_env_file("BASE_REFRESH_TOKEN", BASE_REFRESH_TOKEN)
        update_env_file("ACCESS_TOKEN_EXPIRES_AT", str(ACCESS_TOKEN_EXPIRES_AT))
        # print("新しいアクセストークンを取得しました:", BASE_ACCESS_TOKEN) #デバック環境での確認の際にだけ使用。本番環境では詳細な情報は残さない方が良い
        print("新しいBASEアクセストークンを取得しました。")
    else:
        # print("リフレッシュトークンが期限切れです。再認証を行います。")
        print("アクセストークンの更新に失敗しました:", response.text)

app = Flask(__name__)

@app.route('/')
def home():
    # 認証フローに戻る処理
    return redirect(url_for('authorize'))  # 認証ページにリダイレクト

@app.route('/authorize')
def authorize():
    # 認証ページの処理
    return "ここは認証ページです。"
if __name__ == '__main__':
    app.run(debug=True)

# .envファイルの更新｜.env ファイルに環境変数を書き込む関数
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

# トークンの有効期限を確認
# def check_and_refresh_access_token():
def check_access_token():
    global BASE_ACCESS_TOKEN, BASE_REFRESH_TOKEN, ACCESS_TOKEN_EXPIRES_AT
    if time.time() >= ACCESS_TOKEN_EXPIRES_AT:
        print("BASEアクセストークンが期限切れです。更新を開始します。")
        get_new_access_token()
    else:
        print("BASEアクセストークンは有効です。")

# トークンエラーを処理する関数
def handle_token_error(error_response):
    if error_response.get('error_code') == 'invalid_token':
        print("無効なトークンが検出されました。再認証を実行します。")
        prompt_user_to_reauthenticate()

# 再認証処理を促す関数
def prompt_user_to_reauthenticate():
    # ユーザーに再認証を促す処理（例：新しいトークンを取得する）
    print("ユーザーに再認証を促す処理を行います。")


#-------- ここまではトークン情報と認証情報の確認と更新・取得  ------#

#------------- ここからはNETSEAの商品在庫の確認  ----------#



# BASEの商品情報を取得
def get_base_products():
    base_product_list = []
    # url = f"{BASE_API_URL}/products"
    url = BASE_PRODUCTS_URL
    # headers = {"Authorization": f"Bearer {BASE_ACCESS_TOKEN}"}
    while url:
        response = requests.get(url, headers=base_headers)
        if response.status_code == 200:
            data = response.json()
            for product in data['products']:
                for variation in product.get('variations', []):
                    base_product_list.append({
                        "identifier": product['identifier'],  # BASEの商品コード
                        "variation_identifier": variation['variation_identifier'], # バリエーションの種類コード
                        "variation_stock": variation['variation_stock'] # バリエーションの在庫数
                    })
            url = data.get('next')  # 次のページがあればURLを取得
        else:
            # print("BASE APIから商品情報取得に失敗しました:", response.status_code)
            # print("BASE APIの商品情報取得に失敗しました:", response.text)
            print(f"BASE APIから商品情報取得に失敗しました: {response.status_code}, メッセージ: {response.text}")
            break
    return base_product_list

# BASEの在庫更新
def update_base_product_stock(identifier, variation_identifier, stock_status):
    check_and_refresh_access_token()  # 在庫更新前にトークンを確認
    data = {
        "variation_identifier": variation_identifier,
        "variation_stock": stock_status  # バリエーションごとの在庫を更新
    }
    # headers = {
    #     "Authorization": f"Bearer {BASE_ACCESS_TOKEN}",
    #     "Content-Type": "application/json"
    # }
    url = f"{BASE_API_URL}/products/{identifier}/variations/{variation_identifier}"
    response = requests.put(url, json=data, headers=base_headers)
    if response.status_code == 200:
        print(f"商品 {identifier} の在庫を {stock_status} に更新しました。")
    else:
        print(f"商品 {identifier} の在庫更新に失敗しました:", response.text)





# NETSEA在庫データ取得とBASE更新｜NETSEAの商品情報を取得し、BASEの商品情報と照らし合わせる関数
def update_inventory_from_netsea():
     # BASEの商品データ取得
    # url = f"{BASE_API_URL}/products"
    url = BASE_PRODUCTS_URL
    print("リクエストURL:", url)
    print("リクエストヘッダー:", base_headers)

    # トークンを確認してからAPIリクエストを送信
    response = requests.get(url, headers=base_headers)

    check_and_refresh_access_token()  # トークン確認
    # base_products = get_base_products()  # BASEの商品情報を取得
    if response.status_code == 200:
        base_products = response.json() # BASEの商品情報を取得

        with open('itemdata_4 のコピー.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                direct_item_id = row[0]  # 商品IDが1列目にあると仮定
                print(f"読み込んだ商品ID: {direct_item_id}")

                for base_product in base_products:
                    params = {"direct_item_ids": base_product["identifier"]}
                    netsea_url = f"{NETSEA_API_URL}/items" # 完全なエンドポイントを構築
                    response = requests.get(netsea_url, headers=netsea_headers, params=params)

                    if response.status_code == 200:
                        # print("商品情報を正常に取得しました。")
                        netsea_data = response.json()
                        # base_stock_updates = process_stock_data(netsea_stock_data)
                        base_stock_updates = process_stock_data(netsea_data)

                        for netsea_item in netsea_data['items']:
                            if netsea_item["product_id"] == base_product["identifier"]:
                                stock_status = 0 if netsea_item['sold_out_flag'] == "Y" else 3
                                update_base_product_stock(
                                    base_product['identifier'],
                                    base_product['variation_identifier'],
                                    stock_status
                            )

                        # BASEに在庫情報を送信
                        for update in base_stock_updates:
                            update_url = f"{BASE_API_URL}/products/{update['product_id']}/variations/{update['variation_identifier']}"
                            response = requests.put(update_url, json=update, headers=base_headers)
                            if response.status_code == 200:
                                print("在庫更新成功:", update)
                            else:
                                print("在庫更新失敗:", response.text)

                    else:
                        print("NETSEA APIからの商品情報取得に失敗しました:", response.text)
    else:
        print(f"BASE APIから商品情報取得に失敗しました: {response.status_code}, メッセージ: {response.text}")

# NETSEAの商品データを処理
def process_stock_data(netsea_stock_data):
    base_stock_updates = []
    for item in netsea_stock_data:
        product_id = item['product_id']
        branch_code = item['branch_code']
        sold_out_flag = item['sold_out_flag']

        # 在庫数の設定ルール
        stock_status = 0 if sold_out_flag == "Y" else 3

        # BASE用データの準備
        base_stock_updates.append({
            "product_id": product_id,
            "variation_identifier": branch_code,
            "variation_stock": stock_status
        })
    return base_stock_updates

# 実行
if __name__ == "__main__":
    check_access_token()
    update_inventory_from_netsea()