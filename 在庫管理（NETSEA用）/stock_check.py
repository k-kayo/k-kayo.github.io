import requests
import csv
import os
from dotenv import load_dotenv
import time
pip install waitress
# .envファイルから環境変数を読み込む
load_dotenv()

# NETSEAのアクセストークン
NETSEA_ACCESS_TOKEN = os.getenv("NETSEA_ACCESS_TOKEN")  # .envに設定されたNETSEAトークン

# BASEのアクセストークン
BASE_ACCESS_TOKEN = os.getenv("BASE_ACCESS_TOKEN")  # .envに設定されたBASEトークン

# BASEアクセストークンの有効期限（UNIXタイム）
ACCESS_TOKEN_EXPIRES_AT = float(os.getenv("ACCESS_TOKEN_EXPIRES_AT", 0))

# ヘッダー（NETSEA APIに必要なAuthorizationヘッダー）
headers = {
    "Authorization": f"Bearer {NETSEA_ACCESS_TOKEN}"
}

# BASE APIのURL (在庫情報を更新するため)
# base_api_url = os.getenv('BASE_API_URL')
BASE_API_URL = os.getenv('BASE_API_URL')

# トークンの確認と更新
def check_and_refresh_access_token():
    global BASE_ACCESS_TOKEN, ACCESS_TOKEN_EXPIRES_AT
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
    global BASE_ACCESS_TOKEN, BASE_REFRESH_TOKEN, ACCESS_TOKEN_EXPIRES_AT
    # リフレッシュトークンを使って新しいアクセストークンを取得する処理
    data = {
        # "grant_type": "refresh_token",
        # "client_id": os.getenv("CLIENT_ID"),
        # "client_secret": os.getenv("CLIENT_SECRET"),
        # "refresh_token": os.getenv("BASE_REFRESH_TOKEN"),
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": BASE_REFRESH_TOKEN,
    }
    # response = requests.post("https://api.thebase.in/1/oauth/token", data=data)
    response = requests.post(TOKEN_URL, data=data)
    if response.status_code == 200:
        token_data = response.json()
        BASE_ACCESS_TOKEN = token_data["access_token"]
        expires_in = token_data["expires_in"]
        ACCESS_TOKEN_EXPIRES_AT = time.time() + expires_in

        # トークンを.envに保存
        update_env_file("BASE_ACCESS_TOKEN", BASE_ACCESS_TOKEN)
        update_env_file("BASE_REFRESH_TOKEN", BASE_REFRESH_TOKEN)
        update_env_file("ACCESS_TOKEN_EXPIRES_AT", ACCESS_TOKEN_EXPIRES_AT)
        print("新しいアクセストークンを取得しました:", BASE_ACCESS_TOKEN)
    else:
        print("リフレッシュトークンが期限切れです。再認証を行います。")
        # 認証フローに戻る処理
        return redirect(url_for('authorize'))  # 認証ページにリダイレクト


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

# トークンエラーを処理する関数
def handle_token_error(error_response):
    if error_response.get('error_code') == 'invalid_token':
        print("無効なトークンが検出されました。再認証を実行します。")
        prompt_user_to_reauthenticate()

# 再認証処理を促す関数
def prompt_user_to_reauthenticate():
    # ユーザーに再認証を促す処理（例：新しいトークンを取得する）
    print("ユーザーに再認証を促す処理を行います。")

# 商品ID（テスト用）
direct_item_id = "19794119-2"  # テスト用のダイレクト商品IDに変更

# NETSEA APIのエンドポイントURL (NETSEA)
url = "https://api.netsea.jp/buyer/v1/items/stock"

# NETSEA APIリクエスト
# NETSEA_API_URL = "https://api.netsea.jp/v1/items"  # 実際のAPIエンドポイントに変更
netsea_api_url = os.getenv('NETSEA_API_URL')
# NETSEA_API_URL = os.getenv('NETSEA_API_URL')

params = {
    "direct_item_ids": direct_item_id  # 単一の商品IDを指定
}

def get_base_products():
    base_product_list = []
    # url = "https://api.thebase.in/v2/products"
    url = "https://api.thebase.in/v1/products"

    headers = {"Authorization": f"Bearer {BASE_ACCESS_TOKEN}"}

    while url:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            for product in data['products']:
                for variation in product.get('variations', []):
                    base_product_list.append({
                        "product_id": product['id'],
                        "identifier": product['identifier'],
                        "variation_identifier": variation['variation_identifier'],
                        "variation_stock": variation['variation_stock']
                    })
            url = data.get('next')  # 次ページがある場合、そのURLを取得
        else:
            print(f"BASE API で商品情報を取得できませんでした: {response.status_code}")
            print(response.text)
            break
    return base_product_list

# NETSEAの商品情報を取得し、BASEの商品情報と照らし合わせる関数
# # 商品情報取得関数にトークン確認を追加
def update_inventory_from_netsea():
    # アクセストークンが有効か確認
    check_and_refresh_access_token()  # トークン確認

    # BASEの商品情報を取得
    base_products = get_base_products()

    with open('itemdata_4 のコピー.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            direct_item_id = row[0]  # 商品IDが1列目にあると仮定
            print(f"読み込んだ商品ID: {direct_item_id}")

            # NETSEA APIから商品情報を取得
            params = {
                "direct_item_ids": direct_item_id  # リスト形式で渡す場合は、["ID1", "ID2"]
                # "direct_item_ids": [direct_item_id]  # リスト形式
            }
            # response = requests.get(url, headers=headers, params=params)
            response = requests.get("https://api.netsea.jp/buyer/v1/items", headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()  # JSON形式のレスポンスデータを取得
                # print("レスポンスデータ:", data)  # 取得したデータ全体を確認

                # 必須データが存在するかチェック
                if 'product_id' in data and 'branch_code' in data and 'set_num' in data:
                    # 在庫フラグとセット毎数量の取得
                    sold_out_flag = data.get('sold_out_flg')
                    set_num = data.get('set_num', 0)  # デフォルト値を0に設定

                    # 在庫数を決定
                    if sold_out_flag == 'Y':
                        stock_status = 0  # 売り切れの場合
                    elif sold_out_flag == 'N':
                        stock_status = 3  # 在庫ありの場合
                    else:
                        stock_status = 0  # sold_out_flgがNoneまたは不正な場合もここで設定

                    # NETSEAの商品コードと種類コード
                    netsea_product_code = data['product_id']
                    netsea_product_branch_code = data['branch_code']

                    # BASEの商品と照らし合わせる
                    for base_product in base_products:
                        if (netsea_product_code == base_product.get('identifier') and
                            netsea_product_branch_code == base_product.get('variation_identifier')):
                            # 在庫更新処理
                            update_base_product_stock(base_product['id'], base_product['variation_identifier'], stock_status)
                            break
                else:
                    print("必要なデータがNETSEAのレスポンスに含まれていません。")
            else:
                print(f"NETSEA APIのエラー: {response.status_code}")
                print(response.text)


def update_base_product_stock(product_id, variation_identifier, stock_status):
    check_and_refresh_access_token()  # 在庫更新前にトークンを確認

    data = {
        "variation_identifier": variation_identifier,
        "variation_stock": stock_status  # バリエーションごとの在庫を更新
    }

    headers = {
        "Authorization": f"Bearer {BASE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.put(BASE_API_URL.format(product_id=product_id), json=data, headers=headers)

    if response.status_code == 200:
        print(f"商品ID {product_id} のバリエーション {variation_identifier} の在庫情報が更新されました。")
    else:
        print(f"商品ID {product_id} の在庫更新に失敗しました。エラー: {response.status_code}, {response.text}")


# 実行
update_inventory_from_netsea()

# //テスト目的であった場合//
import requests

def test_base_endpoint():
    url = "https://api.thebase.in/v2/products"
    headers = {
        "Authorization": f"Bearer {BASE_ACCESS_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print("BASE APIエンドポイントが正しいです。")
        print("データ:", response.json())
    else:
        print(f"エラーコード: {response.status_code}, メッセージ: {response.text}")

# エンドポイントをテストする関数を呼び出し
test_base_endpoint()

# //ここまでをテスト後に消す