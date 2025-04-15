from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.schemas.login_schema import LoginRequestSchema
from app.schemas.register_schema import RegisterRequestSchema
from app.schemas.user_schema import UserSchema
from app.services.auth_service import AuthService

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/register', methods=['POST'])
def register():
    schema = RegisterRequestSchema()
    try:
        dto = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    if AuthService.is_email_taken(dto.email):
        return jsonify({'message': 'Користувач вже існує'}), 400

    new_user = AuthService.register_user(dto)
    user_data = UserSchema().dump(new_user)

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

    user = AuthService.authenticate(dto.email, dto.password)
    if not user:
        return jsonify({'message': 'Невірний email або пароль'}), 401

    tokens = AuthService.generate_token_pair(user)
    user_data = UserSchema().dump(user)

    return jsonify({
        **tokens,
        'user': user_data
    })

@auth_routes.route('/refresh', methods=['POST'])
def refresh_token():
    data = request.get_json()
    token = data.get('refresh_token')

    result, error = AuthService.refresh_access_token(token)
    if error:
        return jsonify({'message': error}), 401

    return jsonify(result)
