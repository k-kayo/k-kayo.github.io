from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/callback', methods=['GET'])
def callback():
    # BASEから返された認証コードを取得
    code = request.args.get('code')
    if not code:
        return "Error: No code received", 400  # コードがない場合のエラーメッセージ

    print(f"Received code: {code}")  # ターミナルにコードを表示
    return f"Code received: {code}"  # ブラウザにコードを表示

    # アクセストークンを取得するリクエストをBASEに送る
    token_url = "https://api.thebase.in/1/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": "3c90ae7de5dcd0625a6bc49d56ec2578",  # 実際のクライアントIDに変更
        "client_secret": "64b657790785f360a2e996cab0aad272",  # 実際のクライアントシークレットに変更
        "redirect_uri": "https://miyuka.shopselect.net/callback",  # 実際のコールバックURLに変更
        "code": code
    }
    response = requests.post(token_url, data=data)

    if response.status_code == 200:
        return jsonify(response.json())  # アクセストークンを表示
    else:
        return f"Error: {response.status_code}, {response.text}"

if __name__ == "__main__":
    app.run(port=8000)

