from flask import Blueprint, request
from marshmallow import ValidationError
from app.schemas.login_schema import LoginRequestSchema
from app.schemas.register_schema import RegisterRequestSchema
from app.schemas.user_schema import UserSchema
from app.services.auth_service import AuthService
from app.utils.response_utils import success, error

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/register', methods=['POST'])
def register():
    schema = RegisterRequestSchema()
    try:
        dto = schema.load(request.get_json())
    except ValidationError as err:
        return error("Помилка валідації", err.messages, 400)

    if AuthService.is_email_taken(dto.email):
        return error("Користувач вже існує", status=400)

    new_user = AuthService.register_user(dto)
    user_data = UserSchema().dump(new_user)

    return success("Реєстрація успішна", user_data, status=201)

@auth_routes.route('/login', methods=['POST'])
def login():
    schema = LoginRequestSchema()
    try:
        dto = schema.load(request.get_json())
    except ValidationError as err:
        return error("Помилка валідації", err.messages)

    user = AuthService.authenticate(dto.email, dto.password)
    if not user:
        return error("Невірний email або пароль", status=401)

    tokens = AuthService.generate_token_pair(user)
    user_data = UserSchema().dump(user)

    return success(data={**tokens, "user": user_data})

@auth_routes.route('/refresh', methods=['POST'])
def refresh_token():
    data = request.get_json()
    token = data.get('refresh_token')

    result, error_token = AuthService.refresh_access_token(token)
    if error_token:
        return error(error_token, status=401)

    return success(data=result)
