from flask import Flask
import os

from app.routes import auth_routes, health_bp
from app.models import User
from app.extensions import db
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})  # або вкажи конкретний origin, наприклад: {"http://localhost:3000"}

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'supersecretkey')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(auth_routes)
    app.register_blueprint(health_bp)

    return app
