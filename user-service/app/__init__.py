# user-service/app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Ініціалізація бази даних
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('USER_DATABASE_URL', 'sqlite:///users.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.routes import user_routes
    app.register_blueprint(user_routes)

    with app.app_context():
        from app import models
        db.create_all()

    return app