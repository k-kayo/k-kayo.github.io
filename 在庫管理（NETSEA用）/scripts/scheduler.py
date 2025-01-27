import schedule
import time
from scripts.update_inventory import sync_inventory, check_and_refresh_access_token
from scripts.app import check_and_refresh_access_token

def job():
    check_and_refresh_access_token()  # 定期的にトークンを更新
    sync_inventory("itemdata_4 のコピー.csv")  # 在庫同期も実行

# 毎朝7時に実行（スケジューリング）
schedule.every().day.at("07:00").do(job)
# 1時間ごとにアクセストークンを更新
schedule.every(1).hour.do(check_and_refresh_access_token)

while True:
    schedule.run_pending()
    time.sleep(1)
