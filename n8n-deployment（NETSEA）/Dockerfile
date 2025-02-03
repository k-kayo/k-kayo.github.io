# ベースイメージ
FROM n8nio/n8n:latest

# 作業ディレクトリを設定
WORKDIR /home/node

# 必要な依存関係をインストール
RUN npm install --production

# 環境変数設定
ENV N8N_BASIC_AUTH_ACTIVE=true
ENV N8N_BASIC_AUTH_USER=admin
ENV N8N_BASIC_AUTH_PASSWORD=your_password
ENV N8N_HOST=0.0.0.0
ENV N8N_PORT=5678
ENV N8N_PROTOCOL=https
ENV N8N_SSL_KEY=/path/to/ssl.key
ENV N8N_SSL_CERT=/path/to/ssl.crt


# ポートを公開
EXPOSE 5678

# コンテナ起動時に実行されるコマンド
CMD ["npm", "run", "start"]
