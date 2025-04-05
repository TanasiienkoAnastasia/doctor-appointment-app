# auth-service/app/__init__.py
from flask import Flask
import os
from app.routes import auth_routes
from flask_sqlalchemy import SQLAlchemy
from app.models import User


# Ініціалізація бази даних
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'supersecretkey')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///users.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.register_blueprint(auth_routes)

    with app.app_context():
        from app import models
        db.create_all()

    return app