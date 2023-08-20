from flask import abort, jsonify, request, Blueprint
from flask import current_app as app

import flask_jwt_extended

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

    token = flask_jwt_extended.create_access_token(identity=(user, passwd))

    return jsonify({ 'token': token }), 200
