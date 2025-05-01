from flask import Blueprint, request, current_app
from werkzeug.utils import secure_filename
from marshmallow import ValidationError
import os

from app.schemas import LoginRequestSchema, RegisterRequestSchema, UserSchema
from app.services.auth_service import AuthService
from app.utils import success, error
from swagger_gen.lib.wrappers import swagger_metadata

auth_routes = Blueprint('auth_routes', __name__)


@swagger_metadata(
    summary='Register endpoint',
    description='Цей маршрут реєструє нового користувача з можливістю додати фото.'
)
@auth_routes.route('/register', methods=['POST'])
def register():
    # Розпакування запиту (JSON або multipart/form-data)
    if request.content_type.startswith('multipart/form-data'):
        form_data = request.form.to_dict()
        photo_file = request.files.get('photo')
    else:
        form_data = request.get_json()
        photo_file = None

    # Валідація
    schema = RegisterRequestSchema()
    try:
        dto = schema.load(form_data)
    except ValidationError as err:
        return error("Помилка валідації", err.messages, 400)

    if AuthService.is_email_taken(dto.email):
        return error("Користувач вже існує", status=400)

    # Збереження фото, якщо є
    photo_url = None
    if photo_file and photo_file.filename:
        upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_path, exist_ok=True)

        filename = secure_filename(photo_file.filename)
        photo_path = os.path.join(upload_path, filename)
        photo_file.save(photo_path)

        photo_url = f'/static/uploads/{filename}'

    # Додаємо URL фото в DTO
    dto.photo_url = photo_url

    # Реєстрація
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
