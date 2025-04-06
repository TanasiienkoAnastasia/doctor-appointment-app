from flask import Flask
from app.extensions import db  # нове джерело db
from app.routes import user_routes, health_bp
import os

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('USER_DATABASE_URL', 'sqlite:///users.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(user_routes)
    app.register_blueprint(health_bp)

    with app.app_context():
        from app import models
        db.create_all()

    return app
