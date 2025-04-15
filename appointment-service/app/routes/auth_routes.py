from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.models import User
from app.extensions import db
import jwt
import datetime
import os
from werkzeug.security import check_password_hash
from app.schemas.login_schema import LoginRequestSchema
from app.schemas.user_schema import UserSchema
from app.schemas.register_schema import RegisterRequestSchema

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/register', methods=['POST'])
def register():
    schema = RegisterRequestSchema()
    try:
        dto = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    if User.query.filter_by(email=dto.email).first():
        return jsonify({'message': 'Користувач вже існує'}), 400

    new_user = dto.to_model()

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
    try:
        dto = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    user = User.query.filter_by(email=dto.email).first()
    if not user or not check_password_hash(user.password, dto.password):
        return jsonify({'message': 'Невірний email або пароль'}), 401

    access_exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    refresh_exp = datetime.datetime.utcnow() + datetime.timedelta(days=7)

    access_token = jwt.encode({
        'email': user.email,
        'userType': user.user_type,
        'exp': access_exp
    }, os.getenv('SECRET_KEY'), algorithm='HS256')

    refresh_token = jwt.encode({
        'email': user.email,
        'type': 'refresh',
        'exp': refresh_exp
    }, os.getenv('SECRET_KEY'), algorithm='HS256')

    user_schema = UserSchema()
    user_data = user_schema.dump(user)

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'access_expires': access_exp.isoformat() + 'Z',
        'user': user_data
    })

@auth_routes.route('/refresh', methods=['POST'])
def refresh_token():
    data = request.get_json()
    token = data.get('refresh_token')

    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        if payload.get('type') != 'refresh':
            return jsonify({'message': 'Неправильний тип токена'}), 400
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Термін дії токена вичерпано'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Невалідний токен'}), 400

    access_exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    new_access_token = jwt.encode({
        'email': payload['email'],
        'userType': payload['userType'],
        'exp': access_exp
    }, os.getenv('SECRET_KEY'), algorithm='HS256')

    return jsonify({
        'access_token': new_access_token,
        'access_expires': access_exp.isoformat() + 'Z'
    })
