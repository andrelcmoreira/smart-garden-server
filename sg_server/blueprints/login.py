from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import create_access_token

login_bp = Blueprint('login', __name__, url_prefix='/login')

@login_bp.route('/', methods=['POST'])
def login():
    user = request.json['user']
    pswd = request.json['password']

    if (not user) or (not pswd):
        abort(400, 'invalid user credentials!')

    token = create_access_token(identity=(user, pswd))

    return jsonify({ 'token': token }), 200
