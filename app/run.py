from os import getenv

from flask import Flask
from flask_jwt_extended import JWTManager

from blueprints.devices import devices_bp
#from blueprints.device_config import device_cfg_bp
#from blueprints.device_login import device_login_bp
from blueprints.login import login_bp
from models.mgr import init_db
from error.handlers import *


def create_app():
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = getenv('SECRET_KEY')

    jwt = JWTManager()
    jwt.init_app(app)

    app.register_blueprint(devices_bp)
    #app.register_blueprint(device_cfg_bp)
    #app.register_blueprint(device_login_bp)
    app.register_blueprint(login_bp)

    app.register_error_handler(400, bad_request)
    app.register_error_handler(401, unauthorized_error)
    app.register_error_handler(404, resource_not_found)
    app.register_error_handler(500, internal_error)

    init_db()

    return app


if __name__ == "__main__":
    app = create_app()

    app.run(host='0.0.0.0', debug=True)
