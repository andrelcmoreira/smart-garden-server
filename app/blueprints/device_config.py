from flask import abort, jsonify, request, Blueprint
from flask import current_app as app
from flask_jwt_extended import jwt_required

from storage.models.config import Config
from validators import validate_request, validate_field
from . import CONFIGS_DB, DEVICES_DB

device_cfg_bp = Blueprint('device_config', __name__, url_prefix='/devices')

@device_cfg_bp.route('/<string:dev_id>/config/', methods=['POST'])
@jwt_required()
def config_device(dev_id):
    '''
    POST /devices/<id>/login endpoint implementation.

    :dev_id: ID of device.

    :returns: On success, a success reply; otherwise the suitable error reply
              (see the API documentation for more informations).

    '''
    app.logger.debug(f'device id -> {dev_id}')
    app.logger.debug(f'request payload -> {request.json}')

    if (not validate_field('id', dev_id)) or \
        (not validate_request(request.json)):
        abort(400, 'Bad request')

    if not DEVICES_DB.get(dev_id):
        app.logger.debug(f'device {dev_id} not found on database')
        abort(404, 'Device not registered on database')

    try:
        # mandatory parameters
        interval = request.json['interval']
    except KeyError as key:
        app.logger.debug(f'missing {key} in request')
        abort(400, 'Missing required data')

    cfg = Config(id=dev_id, group=request.json.get('group'), interval=interval)

    CONFIGS_DB.add(cfg)

    return jsonify({ 'msg': 'Configuration registered with success' }), 201

@device_cfg_bp.route('/<string:dev_id>/config/', methods=['GET'])
@jwt_required()
def get_config(dev_id):
    '''
    GET /devices/<id>/config endpoint implementation.

    :dev_id: ID of device.

    :returns: On success, the device configuration; otherwise the suitable error
              reply (see the API documentation for more informations).

    '''
    if (not validate_field('id', dev_id)):
        abort(400, 'Bad request')

    cfg = CONFIGS_DB.get(dev_id)
    if not cfg:
        abort(404, "The config isn't registered on database")

    return jsonify(cfg), 200

@device_cfg_bp.route('/config/', methods=['GET'])
@jwt_required()
def get_configs():
    '''
    GET /devices/config endpoint implementation.

    :returns: On success, all the device configurations; otherwise an empty
              reply.

    '''
    configs = CONFIGS_DB.get_all()

    return jsonify(configs), 200

@device_cfg_bp.route('/<string:dev_id>/config/', methods=['DELETE'])
@jwt_required()
def del_config(dev_id):
    '''
    DELETE /devices/<id>/config endpoint implementation.

    :dev_id: ID of device.

    :returns: On success, a success reply; otherwise the suitable error reply
              (see the API documentation for more informations).

    '''
    app.logger.debug(f'device id -> {dev_id}')

    if not validate_field('id', dev_id):
        abort(400, 'Bad request')

    if not CONFIGS_DB.get(dev_id):
        app.logger.debug(f'config for device {dev_id} not found')
        abort(404, "There's no config for the specific device")

    CONFIGS_DB.rm(dev_id)

    return jsonify({ 'msg': 'Config deleted from database' }), 200

@device_cfg_bp.route('/<string:dev_id>/config/', methods=['PUT'])
@jwt_required()
def update_config(dev_id):
    '''
    PUT /devices/<id>/config endpoint implementation.

    :dev_id: ID of device.

    :returns: On success, a success reply; otherwise the suitable error reply
              (see the API documentation for more informations).

    '''
    app.logger.debug(f'device id -> {dev_id}')

    if (not validate_field('id', dev_id)) or \
        (not validate_request(request.json)):
        abort(400, 'Bad request')

    try:
        # mandatory parameters
        param = request.json['param']
        val = request.json['value']
    except KeyError as key:
        app.logger.debug(f'missing {key} in request')
        abort(400, 'Missing required data')

    if not CONFIGS_DB.get(dev_id):
        app.logger.debug(f'config for device {dev_id} not found')
        abort(404, "There's no config for the specific device")

    CONFIGS_DB.update(dev_id, param, val)

    return jsonify({ 'msg': 'Config updated in database' }), 200
