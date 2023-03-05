from flask import abort, current_app, jsonify, request, Blueprint

import flask_jwt_extended

from app.validators import validate_request

login_bp = Blueprint('login', __name__, url_prefix='/login')

@login_bp.route('/', methods=['POST'])
def login():
    current_app.logger.debug('request payload: %s' % request.json)

    if not validate_request(request.json):
        abort(400, 'Invalid user credentials')

    try:
        user = request.json['user']
        passwd = request.json['password']
    except KeyError as e:
        current_app.logger.debug('missing %s in request' % e)
        abort(400, 'Missing required data')

    token = flask_jwt_extended.create_access_token(identity=(user, passwd))

    return jsonify({ 'token': token }), 200
