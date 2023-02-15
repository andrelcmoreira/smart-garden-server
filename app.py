from flask import Flask

from sg_server.blueprints.devices import devices_bp
from sg_server.error.handlers import *

def create_app():
    app = Flask(__name__)

    app.register_blueprint(devices_bp)

    app.register_error_handler(400, bad_request)
    app.register_error_handler(404, resource_not_found)

    return app

if __name__ == "__main__":
    app = create_app()

    app.run(debug=True)
