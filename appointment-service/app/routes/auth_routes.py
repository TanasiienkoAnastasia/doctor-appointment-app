from flask import Blueprint, request, jsonify
from app.models import User
from app.extensions import db
import jwt
import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
from app.dto.user_dto import UserDTO

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

    hashed_password = generate_password_hash(password)

    new_user = User(
        username=username,
        email=email,
        password =hashed_password,
        user_type=user_type
    )

    db.session.add(new_user)
    db.session.commit()

    user_dto = UserDTO.from_model(new_user)

    return jsonify({
        'message': 'Реєстрація успішна',
        'user': user_dto.to_dict()
    }), 201

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Невірний email або пароль'}), 401

    token_payload = {
        'email': user.email,
        'userType': user.user_type,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }

    token = jwt.encode(token_payload, os.getenv('SECRET_KEY'), algorithm='HS256')

    user_dto = UserDTO.from_model(user)

    return jsonify({
        'token': token,
        'user': user_dto.to_dict()
    })
