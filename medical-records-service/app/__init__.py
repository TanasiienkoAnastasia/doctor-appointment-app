from flask import Flask
from app.extensions import db
from app.routes import medical_routes, health_bp
import os

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('MEDICAL_DB_URL', 'sqlite:///medical.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(medical_routes)  # якщо є маршрути
    app.register_blueprint(health_bp)       # 🩺 health-check

    with app.app_context():
        from app import models
        db.create_all()

    return app
