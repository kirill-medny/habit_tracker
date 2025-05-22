import secrets

secret_key = secrets.token_urlsafe(32)  # 32 bytes gives 256 bits
print(secret_key)
