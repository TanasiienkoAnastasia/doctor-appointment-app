import datetime
import jwt
import os
from werkzeug.security import check_password_hash
from app.models import User
from app.extensions import db


class AuthService:
    @staticmethod
    def authenticate(email, password):
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return None
        return user

    @staticmethod
    def is_email_taken(email):
        return User.query.filter_by(email=email).first() is not None

    @staticmethod
    def register_user(dto):
        new_user = dto.to_model()
        db.session.add(new_user)
        db.session.commit()
        return new_user