from flask import Flask
import os
from app.extensions import db
from app.routes import health_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('NOTIFY_DB_URL', 'sqlite:///notify.db')
    db.init_app(app)
    app.register_blueprint(health_bp)
    return app

