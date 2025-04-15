from flask import Flask
from app.extensions import db
from app.routes.auth_routes import auth_routes
from app.routes.appointment_routes import appointment_routes
from app.routes.notification_routes import notification_routes
from app.routes.user_routes import user_routes
from app.routes.medical_records_routes import medical_records_routes
from app.routes.schedule_routes import schedule_routes
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'supersecretkey')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(auth_routes, url_prefix='/auth')
    app.register_blueprint(appointment_routes, url_prefix='/appointments')
    app.register_blueprint(medical_records_routes, url_prefix='/medical_records')
    app.register_blueprint(schedule_routes, url_prefix='/schedule')
    app.register_blueprint(notification_routes, url_prefix='/notification')
    app.register_blueprint(user_routes, url_prefix='/user')

    with app.app_context():
        db.create_all()

    return app
