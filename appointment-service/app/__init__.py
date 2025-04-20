import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.extensions import db
from app.routes import (
    auth_routes,
    doctor_routes,
    patient_appointments_routes,
    recommendation_routes,
    user_routes
)
from swagger_gen.swagger import Swagger

def create_app():
    load_dotenv(override=True)

    print("Loaded DB URI:", os.getenv('DATABASE_URL'))

    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    swagger = Swagger(
        app=app,
        title='app'
    )
    swagger.configure()

    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_SECRET_KEY"] = os.getenv('SECRET_KEY', 'supersecretkey')
    wt = JWTManager(app)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'supersecretkey')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(auth_routes, url_prefix='/auth')
    app.register_blueprint(patient_appointments_routes, strict_slashes=False)
    app.register_blueprint(user_routes, url_prefix='/user')
    app.register_blueprint(doctor_routes, url_prefix='/doctor')
    app.register_blueprint(recommendation_routes)

    with app.app_context():
        # db.drop_all() Uncomment to drop db
        db.create_all()

    return app
