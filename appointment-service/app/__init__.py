# appointment-service/app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('APPOINTMENT_DATABASE_URL', 'sqlite:///appointments.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.routes import appointment_routes
    app.register_blueprint(appointment_routes)

    with app.app_context():
        from app import models
        db.create_all()

    return app