from flask import abort, jsonify, request, Blueprint
from flask import current_app as app
from hashlib import sha256

import flask_jwt_extended

from models.user_handler import UserHandler
from validators import validate_request


login_bp = Blueprint('login', __name__, url_prefix='/login')


@login_bp.route('/', methods=['POST'])
def login():
    '''
    POST /login endpoint implementation.

    :returns: On success, the access token; otherwise the suitable error reply
              (see the API documentation for more informations).

    '''
    app.logger.debug(f'request payload: {request.json}')

    if not validate_request(request.json):
        abort(400, 'Invalid user credentials')

    try:
        # mandatory parameters
        user = request.json['user']
        passwd = request.json['password']
    except KeyError as key:
        app.logger.debug(f'missing {key} in request')
        abort(400, 'Missing required data')

    ret = UserHandler.get(user)
    if not ret or (ret.passwd != sha256(passwd.encode('utf-8')).hexdigest()):
        app.logger.debug(f'invalid login credentials "{user}, {passwd}"')
        abort(401, 'Bad credentials!')

    token = flask_jwt_extended.create_access_token(identity=(user, passwd))

    return jsonify({ 'token': token }), 200
