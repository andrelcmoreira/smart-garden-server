from flask import Flask
from app.devices import devices_bp

app = Flask(__name__)

app.register_blueprint(devices_bp)
