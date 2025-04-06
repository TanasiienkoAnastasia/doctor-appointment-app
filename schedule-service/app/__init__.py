from flask import Flask
from app.extensions import db
from app.routes import schedule_routes, health_bp
import os

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SCHEDULE_DB_URL', 'sqlite:///schedule.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(schedule_routes)
    app.register_blueprint(health_bp)

    with app.app_context():
        from app import models
        db.create_all()

    return app
