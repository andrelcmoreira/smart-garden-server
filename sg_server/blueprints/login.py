from flask import Blueprint, request, jsonify, abort

#from flask_jwt_extended import create_access_token
import flask_jwt_extended

login_bp = Blueprint('login', __name__, url_prefix='/login')

@login_bp.route('/', methods=['POST'])
def login():
    user = request.json.get('user')
    passwd = request.json.get('password')

    if (not user) or (not passwd):
        abort(400, 'invalid user credentials!')

    token = flask_jwt_extended.create_access_token(identity=(user, passwd))

    return jsonify({ 'token': token }), 200
