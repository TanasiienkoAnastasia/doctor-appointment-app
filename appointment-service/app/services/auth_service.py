import datetime
import jwt
import os
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from app.models.user import User
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

    @staticmethod
    def generate_token(data, expires_delta, token_type="access"):
        payload = {**data, 'exp': datetime.datetime.utcnow() + expires_delta}
        if token_type == 'refresh':
            payload['type'] = 'refresh'
        return jwt.encode(payload, os.getenv('JWT_SECRET', 'jwt-default'), algorithm='HS256')

    @staticmethod
    def generate_token_pair(user):
        access_exp = datetime.timedelta(minutes=15)
        refresh_exp = datetime.timedelta(days=7)

        access_token = create_access_token(identity=user.email, expires_delta=access_exp, additional_claims={
            'email': user.email,
            'name': user.name,
            'surname': user.surname,
            'middle_name': user.middle_name,
            'userType': user.user_type,
            'id': user.id
        })

        refresh_token = AuthService.generate_token({
            'email': user.email,
            'userType': user.user_type
        }, refresh_exp, token_type='refresh')

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'access_expires': (datetime.datetime.utcnow() + access_exp).isoformat() + 'Z'
        }

    @staticmethod
    def refresh_access_token(refresh_token):
        try:
            payload = jwt.decode(refresh_token, os.getenv('JWT_SECRET', 'jwt-default'), algorithms=['HS256'])
            if payload.get('type') != 'refresh':
                return None, 'Неправильний тип токена'
        except jwt.ExpiredSignatureError:
            return None, 'Термін дії токена вичерпано'
        except jwt.InvalidTokenError:
            return None, 'Невалідний токен'

        access_exp = datetime.timedelta(minutes=15)
        new_token = AuthService.generate_token({
            'email': payload['email'],
            'userType': payload['userType']
        }, access_exp)

        return {
            'access_token': new_token,
            'access_expires': (datetime.datetime.utcnow() + access_exp).isoformat() + 'Z'
        }, None