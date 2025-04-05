from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.routes import notify_routes
    app.register_blueprint(notify_routes)

    return app
