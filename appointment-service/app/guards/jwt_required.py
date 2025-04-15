import os
from functools import wraps
import jwt
from flask import request, jsonify

def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'message': 'Неавторизовано'}), 401
        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])
            request.user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Термін дії токена вичерпано'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Невалідний токен'}), 401
        return f(*args, **kwargs)
    return wrapper
