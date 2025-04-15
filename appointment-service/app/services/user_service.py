from app.models import User
from app.schemas import UserSchema


class UserService:
    @staticmethod
    def get_user_by_id(user_id):
        user = User.query.get(user_id)
        if not user:
            return None
        return UserSchema().dump(user)

    @staticmethod
    def get_all_users():
        users = User.query.all()
        return UserSchema(many=True).dump(users)