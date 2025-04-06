# auth-service/app/routes.py
from flask import request, jsonify
from flask import Blueprint

auth_routes = Blueprint('auth_routes', __name__)

import jwt
import datetime
import os
from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK'}), 200


users_db = {}

@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users_db:
        return jsonify({'message': 'Користувач вже існує'}), 400

    users_db[username] = password
    return jsonify({'message': 'Реєстрація успішна'})

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if users_db.get(username) != password:
        return jsonify({'message': 'Невірний логін або пароль'}), 401

    token = jwt.encode({
        'user': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }, os.getenv('SECRET_KEY', 'supersecretkey'), algorithm='HS256')

    return jsonify({'token': token})