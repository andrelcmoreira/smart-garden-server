from flask import abort, jsonify, request, Blueprint
from flask import current_app as app

import flask_jwt_extended

from db.models.config import Config
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

    with app.db.cursor() as cursor:
        cursor.execute(f'select * from devices where id = {dev_id}')

        ret = cursor.fetchone()
        if not ret:
            app.logger.debug(f'device {dev_id} not found')
            abort(404, "The device isn't registered on database")

        app.logger.debug(f'found device -> {ret}')

        if ret[1] != serial:
            app.logger.debug(
                f"incorrect serial number '{serial}' for device '{dev_id}'"
            )
            abort(401, 'Authentication failed')

        cursor.execute(f'select * from configs where dev_id = {dev_id}')

        ret = cursor.fetchone()
        if not ret:
            app.logger.debug(f'device {dev_id} has no config')
            abort(404, "There's no config for the specific device")

        app.logger.debug(f'found config -> {ret}')

    token = flask_jwt_extended.create_access_token(identity=(dev_id, serial))
    cfg = Config(id=ret[1], interval=ret[3], group=ret[2])

    return jsonify(
        {
            'msg': 'Device authenticated with success',
            'token': token,
            'config': cfg
        }
    ), 200
