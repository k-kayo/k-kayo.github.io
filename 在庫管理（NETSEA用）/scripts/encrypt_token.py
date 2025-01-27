from cryptography.fernet import Fernet

# 生成されたENCRYPTION_KEYを使用
encryption_key = "O71XSNYte6lv0y-Dcs8gPeSYrH9BpTdV84wG4Ep3M94="
fernet = Fernet(encryption_key.encode())

# 暗号化するAPIトークン
api_token = "ENCRYPTION_KEY"
encrypted_api_token = fernet.encrypt(api_token.encode()).decode('utf-8')

print("ENCRYPTED_API_TOKEN:", encrypted_api_token)
