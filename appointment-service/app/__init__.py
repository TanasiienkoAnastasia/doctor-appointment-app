from dotenv import load_dotenv
from flask import Flask
from app.extensions import db
from app.routes.auth_routes import auth_routes
from app.routes.appointment_routes import appointment_routes
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
    app.register_blueprint(appointment_routes, url_prefix='/appointments')
    app.register_blueprint(user_routes, url_prefix='/user')

    with app.app_context():
        db.drop_all()
        db.create_all()

    return app
