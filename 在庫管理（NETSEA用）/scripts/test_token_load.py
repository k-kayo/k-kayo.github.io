import json

# access_token.json からトークンデータを読み込む
with open("access_token.json", "r", encoding="utf-8") as file:
    token_data = json.load(file)  # JSONデータを辞書形式で読み込む

# トークン情報を表示（確認用）
print("Access Token:", token_data["access_token"])
print("Expires At:", token_data["expires_at"])