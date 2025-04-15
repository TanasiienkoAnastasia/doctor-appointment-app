from flask import Flask
from app.extensions import db
from app.routes.auth_routes import auth_routes
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})  # або вкажи конкретний origin, наприклад: {"http://localhost:3000"}

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'supersecretkey')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(auth_routes)

    with app.app_context():
        db.create_all()

    return app
