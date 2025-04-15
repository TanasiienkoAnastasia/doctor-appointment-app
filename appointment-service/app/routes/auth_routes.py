from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from app.models import User
from app.extensions import db
import jwt
import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
from app.schemas.login_schema import LoginRequestSchema
from app.schemas.user_schema import UserSchema
from app.schemas.register_schema import RegisterRequestSchema

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/register', methods=['POST'])
def register():
    schema = RegisterRequestSchema()
    try:
        dto = schema.load(request.get_json())  # ⬅️ отримаємо RegisterRequestDTO
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    existing_user = User.query.filter_by(email=dto.email).first()
    if existing_user:
        return jsonify({'message': 'Користувач вже існує'}), 400

    hashed_password = generate_password_hash(dto.password)

    new_user = User(
        username=dto.name,
        email=dto.email,
        password=hashed_password,
        user_type=dto.user_type
    )

    db.session.add(new_user)
    db.session.commit()

    user_schema = UserSchema()
    user_data = user_schema.dump(new_user)

    return jsonify({
        'message': 'Реєстрація успішна',
        'user': user_data
    }), 201

@auth_routes.route('/login', methods=['POST'])
def login():
    schema = LoginRequestSchema()
    json_data = request.get_json()

    errors = schema.validate(json_data)
    if errors:
        return jsonify({'errors': errors}), 400

    email = json_data['email']
    password = json_data['password']

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Невірний email або пароль'}), 401

    token_payload = {
        'email': user.email,
        'userType': user.user_type,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }

    token = jwt.encode(token_payload, os.getenv('SECRET_KEY'), algorithm='HS256')
    user_schema = UserSchema()
    user_data = user_schema.dump(user)

    return jsonify({
        'token': token,
        'user': user_data
    })
