from flask import Blueprint, request, jsonify
from app.models import User
from app.extensions import db
import jwt
import datetime
import os

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('name')
    email = data.get('email')
    password = data.get('password')
    user_type = data.get('userType')

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'Користувач вже існує'}), 400

    new_user = User(
        username=username,
        email=email,
        password=password,  # 🔐 можна додати хешування
        user_type=user_type
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Реєстрація успішна'}), 201

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or user.password != password:
        return jsonify({'message': 'Невірний email або пароль'}), 401

    token_payload = {
        'email': user.email,
        'userType': user.user_type,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }

    token = jwt.encode(token_payload, os.getenv('SECRET_KEY'), algorithm='HS256')

    return jsonify({'token': token})