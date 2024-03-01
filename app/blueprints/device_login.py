from flask import abort, jsonify, request, Blueprint
from flask import current_app as app

import flask_jwt_extended

from models.device_handler import DeviceHandler
from models.config_handler import ConfigHandler
from validators import validate_request


device_login_bp = Blueprint('device_login', __name__, url_prefix='/devices')


@device_login_bp.route('/login/', methods=['POST'])
def login_device():
    '''
    POST /devices/login endpoint implementation.

    :returns: On success, the device token and the device configuration;
              otherwise the suitable error reply (see the API documentation for
              more informations).

    '''
    app.logger.debug(f'request payload -> {request.json}')

    if not validate_request(request.json):
        abort(400, 'Bad request')

    try:
        # mandatory parameters
        dev_id = request.json['id']
        serial = request.json['serial-number']
    except KeyError as key:
        app.logger.debug(f"missing '{key}' in request")
        abort(400, 'Missing required data')

    dev = DeviceHandler.get(dev_id)
    if not dev:
        app.logger.debug(f'device {dev_id} not found')
        abort(404, "The device isn't registered on database")

    app.logger.debug(f'found device with id {dev_id}: {dev}')

    if dev.serial != serial:
        app.logger.debug(
            f"incorrect serial number '{serial}' for device '{dev_id}'"
        )
        abort(401, 'Authentication failed')

    cfg = ConfigHandler.get(dev_id)
    if not cfg:
        app.logger.debug(f'device {dev_id} has no config')
        abort(404, "There's no config for the specific device")

    app.logger.debug(f'found config -> {cfg}')

    token = flask_jwt_extended.create_access_token(identity=(dev_id, serial))

    return jsonify(
        {
            'msg': 'Device authenticated with success',
            'token': token,
            'config': cfg
        }
    ), 200
