import requests
import csv
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# NETSEAのアクセストークン
NETSEA_ACCESS_TOKEN = os.getenv("NETSEA_ACCESS_TOKEN")  # .envに設定されたNETSEAトークン

# ヘッダー（NETSEA APIに必要なAuthorizationヘッダー）
headers = {
    "Authorization": f"Bearer {NETSEA_ACCESS_TOKEN}"
}

# 商品ID（テスト用）
direct_item_id = "19794119-2"  # テスト用のダイレクト商品IDに変更

# BASEのアクセストークン
BASE_ACCESS_TOKEN = os.getenv("BASE_ACCESS_TOKEN")  # .envに設定されたBASEトークン

# NETSEA APIのエンドポイントURL (NETSEA)
url = "https://api.netsea.jp/buyer/v1/items/stock"

# BASE APIのURL (在庫情報を更新するため)
BASE_API_URL = "https://api.thebase.in/v1/products/{product_id}"



# NETSEA APIリクエスト
# NETSEA_API_URL = "https://api.netsea.jp/v1/items"  # 実際のAPIエンドポイントに変更
NETSEA_API_URL = "https://api.netsea.jp/buyer/v1/items"


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
def update_inventory_from_netsea():
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
            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()  # JSON形式のレスポンスデータを取得
                print("レスポンスデータ:", data)  # 取得したデータ全体を確認

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

