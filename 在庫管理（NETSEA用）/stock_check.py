import requests
import csv

# APIのエンドポイントURL
url = "https://api.netsea.jp/buyer/v1/items/stock"

# ヘッダー（Bearerトークンをここに入れます）
headers = {
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjVkOWE3NWI2OTZmNmVlMDA4ZjZlNDZkNDA0YzcxMWUxYzVjYTRmZmZhNGIzODliYWRkNWZhOGFjNmZiMDcwMDI4Y2U2MzQ2Y2YwNjU3NDUwIn0.eyJhdWQiOiIzNTMxIiwianRpIjoiNWQ5YTc1YjY5NmY2ZWUwMDhmNmU0NmQ0MDRjNzExZTFjNWNhNGZmZmE0YjM4OWJhZGQ1ZmE4YWM2ZmIwNzAwMjhjZTYzNDZjZjA2NTc0NTAiLCJpYXQiOjE3MzIyNTQ5OTYsIm5iZiI6MTczMjI1NDk5NiwiZXhwIjoxNzQ3ODA2OTk2LCJzdWIiOiI4OTkwNzMiLCJzY29wZXMiOltdfQ.I42EeX_EDxwU_9az1k8lybfi-05qPZKk-2lQaGos2G9bzj8NPKiHMTRv7E9g54tOuc1gjW90gl1A_UTi2sEv-NBUGsJ3S_YbtSCV97duV6zlp484MSG7indxVZpgxy1ZPN-4OtcKt3fYU2m6tNoahKxw3xeZs61KQ1Hg05EMeF7kRv1bG_jelVgzcPrm7D2CnmcE6TH9oqvpfx8uPBJajz-NXog7KEV9cgv76gbY0QrzC4Cv5qsVPUs7hmOWFKUpecATwl7opaevqzs-IqujJ-xsbyFJ3NzVvN7K6-3rC5xDq0aRdfoXMqMnI19jW-xIZFBdye5IopLu8PQHJmUPnZ9UBpHYPYtC88iK2suBz5H5_K3cq1m7r_py7D7Xd4RYJngFgVsxa8tJFVU8pmTLgQIxHnlRJZzK4xnffrYYrjwi0Izv0qqqmzp5GN6QAjcrcHMgS-zv_RHhwFgURuibMj-ht734Uzc-I7AM_WWSma_OvsNNycXJ1b4cKbCMPljPOQOOn_Wif8BAL7QCSKob8wLLPIeJnq7E1JR-1KivYYcKRcewyv6rjJrik76V4Gb7pMj_7dGByE4N-T6mkk4F9GuNzQdG3GwEeP8FeRFW5y0IHIMnb8qzqjmKdeD9MSqAnCloJgmrurCZjGF5TaKVvUKg6hTkyKN9faCdLoRFrcs"
}
# CSVファイルからダイレクト商品IDを読み込む
with open('itemdata_4.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        direct_item_id = row[0]  # 商品IDが1列目にあると仮定

        # リクエストのパラメータとして直接アイテムIDを設定
        params = {
            "direct_item_id": direct_item_id
        }

        # APIリクエストを送信
        response = requests.get(url, headers=headers, params=params)

        # レスポンスの表示
        if response.status_code == 200:
            data = response.json()  # JSON形式のレスポンスデータを取得
            print("レスポンスデータ:", data)  # 返ってきたデータ全体を表示
            if 'direct_item_id' in data:
                print(f"商品ID: {data['direct_item_id']}")
            else:
                print("direct_item_id がレスポンスに含まれていません")
        else:
            print(f"エラーが発生しました: {response.status_code}")  # エラーコードを表示



            # BASE APIの設定
BASE_API_URL = "https://api.thebase.in/v2/products/{product_id}"
BASE_ACCESS_TOKEN = "your_base_access_token"

# BASE APIの商品更新関数
def update_base_product_stock(product_id, stock_status):
    data = {
        "product": {
            "stock": stock_status  # 在庫数を設定（在庫ありなら10、売り切れなら0）
        }
    }

    headers = {
        "Authorization": f"Bearer {BASE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.put(BASE_API_URL.format(product_id=product_id), json=data, headers=headers)

    if response.status_code == 200:
        print(f"商品ID {product_id} の在庫情報が更新されました。")
    else:
        print(f"商品ID {product_id} の在庫更新に失敗しました。エラー: {response.status_code}, {response.text}")

# NETSEAから在庫情報を取得してBASEに反映させる関数
def update_inventory_from_netsea():
    with open('itemdata_4.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            direct_item_id = row[0]  # CSVファイルから商品IDを読み込む

            # NETSEAから商品情報を取得
            params = {"direct_item_id": direct_item_id}
            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()
                item_id = data.get('direct_item_id')
                sold_out_flag = data.get('sold_out_flg')

                # 在庫数を決める
                if sold_out_flag == 'N':
                    stock_status = 10  # 在庫ありの時は10個など適切な数を設定
                elif sold_out_flag == 'Y':
                    stock_status = 0  # 売り切れの場合は0
                else:
                    stock_status = 0  # 不明な場合も0

                # BASEに在庫情報を更新
                update_base_product_stock(item_id, stock_status)
            else:
                print(f"NETSEAのAPIエラー: {response.status_code}, {response.text}")

# 実行
update_inventory_from_netsea()
