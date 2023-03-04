from flask import Blueprint, request, jsonify, abort

from flask_jwt_extended import create_access_token
#import flask_jwt_extended

from app.validators import validate_request

login_bp = Blueprint('login', __name__, url_prefix='/login')

@login_bp.route('/', methods=['POST'])
def login():
    if not validate_request(request.json):
        abort(400, 'Invalid user credentials')

    user = request.json.get('user')
    passwd = request.json.get('password')
    token = create_access_token(identity=(user, passwd))

    return jsonify({ 'token': token }), 200
