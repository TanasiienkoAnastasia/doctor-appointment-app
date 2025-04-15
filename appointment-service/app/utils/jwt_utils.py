import os
from datetime import datetime
import jwt

def generate_token(data, expires_delta, token_type="access"):
    payload = {**data, 'exp': datetime.utcnow() + expires_delta}
    if token_type == 'refresh':
        payload['type'] = 'refresh'
    return jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm='HS256')