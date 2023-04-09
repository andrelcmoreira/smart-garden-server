from os import getenv

from flask import Flask
from flask_jwt_extended import JWTManager

from app.blueprints.devices import devices_bp
from app.blueprints.device_config import device_cfg_bp
from app.blueprints.device_login import device_login_bp
from app.blueprints.login import login_bp
from app.error.handlers import *

def create_app():
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = getenv('SECRET_KEY')

    jwt = JWTManager()
    jwt.init_app(app)

    app.register_blueprint(devices_bp)
    app.register_blueprint(device_cfg_bp)
    app.register_blueprint(device_login_bp)
    app.register_blueprint(login_bp)

    app.register_error_handler(400, bad_request)
    app.register_error_handler(401, unauthorized_error)
    app.register_error_handler(404, resource_not_found)
    app.register_error_handler(500, internal_error)

    return app

if __name__ == "__main__":
    app = create_app()

    app.run(debug=True)
