import datetime
import os
import jwt
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from werkzeug.security import check_password_hash
from app.extensions import db
from app.models import User
from app.schemas.login_schema import LoginRequestSchema
from app.schemas.register_schema import RegisterRequestSchema
from app.schemas.user_schema import UserSchema
from app.utils.jwt_utils import generate_token

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

    access_exp_delta = datetime.timedelta(minutes=15)

    access_token = generate_token({'email': user.email, 'userType': user.user_type}, access_exp_delta)
    refresh_token = generate_token({'email': user.email, 'type': 'refresh'}, datetime.timedelta(days=7), token_type='refresh')

    user_schema = UserSchema()
    user_data = user_schema.dump(user)

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'access_expires': (datetime.datetime.utcnow() + access_exp_delta).isoformat() + 'Z',
        'user': user_data
    })

@auth_routes.route('/refresh', methods=['POST'])
def refresh_token():
    data = request.get_json()
    token = data.get('refresh_token')

    try:
        payload = jwt.decode(token, os.getenv('JWT_SECRET', 'jwt-default'), algorithms=['HS256'])
        if payload.get('type') != 'refresh':
            return jsonify({'message': 'Неправильний тип токена'}), 400
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Термін дії токена вичерпано'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Невалідний токен'}), 400

    access_exp_delta = datetime.timedelta(minutes=15)
    new_access_token = generate_token({'email': payload['email'], 'userType': payload['userType']}, access_exp_delta)

    return jsonify({
        'access_token': new_access_token,
        'access_expires': (datetime.datetime.utcnow() + access_exp_delta).isoformat() + 'Z'
    })
