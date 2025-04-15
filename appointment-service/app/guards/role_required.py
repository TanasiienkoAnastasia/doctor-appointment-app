import os
from functools import wraps

import jwt
from flask import request, jsonify


def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'message': 'Токен відсутній'}), 401

            try:
                payload = jwt.decode(token.split(" ")[1], os.getenv('JWT_SECRET'), algorithms=['HS256'])
                if payload['userType'] != required_role:
                    return jsonify({'message': 'Недостатньо прав'}), 403
            except:
                return jsonify({'message': 'Невалідний токен'}), 401

            return f(*args, **kwargs)
        return wrapper
    return decorator
