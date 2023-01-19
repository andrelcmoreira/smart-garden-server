from flask import Flask
from app.register import register_bp

app = Flask(__name__)

app.register_blueprint(register_bp)
