from dotenv import load_dotenv
from flask import Flask
from app.extensions import db
from app.routes.auth_routes import auth_routes
from app.routes.patient_appointments_routes import patient_appointments_routes
from app.routes.recommendation_routes import recommendation_routes
from app.routes.doctor_routes import doctor_routes
from app.routes.user_routes import user_routes
from flask_cors import CORS
from swagger_gen.swagger import Swagger
import os

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
