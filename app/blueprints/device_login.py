from flask import abort, jsonify, request, Blueprint
from flask import current_app as app

import flask_jwt_extended

from app.validators import validate_request, validate_field
from . import DEVICES_DB, CONFIGS_DB

device_login_bp = Blueprint('device_login', __name__, url_prefix='/devices')

@device_login_bp.route('/login/', methods=['POST'])
def login_device():
    '''
    TODO

    '''
    app.logger.debug(f'request payload -> {request.json}')

    if not validate_request(request.json):
        abort(400, 'Bad request')

    try:
        dev_id = request.json['id']
        serial = request.json['serial-number']
    except KeyError as key:
        app.logger.debug(f"missing '{key}' in request")
        abort(400, 'Missing required data')

    dev = DEVICES_DB.get(dev_id)
    if not dev:
        app.logger.debug(f"device '{dev_id}' not found on database")
        abort(404, 'Device not registered in database')

    if dev['serial'] != serial:
        app.logger.debug(
            f"incorrect serial number '{serial}' for device '{dev_id}'"
        )
        abort(401, 'Authentication failed')

    cfg = CONFIGS_DB.get(dev_id)
    if not cfg:
        app.logger.debug(f"no config for '{dev_id}'")
        abort(404, "There's no config for the specified device")

    token = flask_jwt_extended.create_access_token(identity=(dev_id, serial))

    return jsonify(
        {
            'msg': 'Device authenticated with success',
            'token': token,
            'config': cfg
        }
    ), 200
