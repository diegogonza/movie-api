from jwt import encode, decode

def create_token(data: dict) -> str:
    token: str = encode(payload= data, key= 'my_secret_key', algorithm='HS256')
    return token

def validate_token(token) -> dict:
    data: dict = decode(token, key= 'my_secret_key', algorithm='HS256')
    return data