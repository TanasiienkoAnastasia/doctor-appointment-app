from flask import Blueprint
from app.guards.jwt_required import jwt_required
from app.services.user_service import UserService
from app.utils.response_utils import success, error

user_routes = Blueprint('user_routes', __name__)

@jwt_required
@user_routes.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user_data = UserService.get_user_by_id(user_id)
    if not user_data:
        return error("Користувача не знайдено", status=404)
    return success(data=user_data)

@jwt_required
@user_routes.route('/users', methods=['GET'])
def get_all_users():
    user_list = UserService.get_all_users()
    return success(data=user_list)
