from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SCHEDULE_DB_URL', 'sqlite:///schedule.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.routes import schedule_routes
    app.register_blueprint(schedule_routes)

    with app.app_context():
        from app import models
        db.create_all()

    return app
