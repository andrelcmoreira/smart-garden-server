from flask import abort, jsonify, request, Blueprint
from flask import current_app as app
from flask_jwt_extended import jwt_required

from models.entities.config import Config
from models.device_handler import DeviceHandler
from models.config_handler import ConfigHandler
from validators import validate_request, validate_field


device_cfg_bp = Blueprint('device_config', __name__, url_prefix='/devices')


@device_cfg_bp.route('/<string:dev_id>/config/', methods=['POST'])
@jwt_required()
def config_device(dev_id):
    '''
    POST /devices/<id>/config endpoint implementation.

    :dev_id: ID of device.

    :returns: On success, a success reply; otherwise the suitable error reply
              (see the API documentation for more informations).

    '''
    app.logger.debug(f'device id -> {dev_id}')
    app.logger.debug(f'request payload -> {request.json}')

    if (not validate_field('id', dev_id)) or \
        (not validate_request(request.json)):
        abort(400, 'Bad request')

    try:
        # mandatory parameters
        interval = request.json['interval']
    except KeyError as key:
        app.logger.debug(f'missing {key} in request')
        abort(400, 'Missing required data')

    group = request.json.get('group') # optional

    if not DeviceHandler.entry_exists(dev_id):
        app.logger.debug(f'device {dev_id} not found')
        abort(404, "The device isn't registered on database")

    app.logger.debug(f'found device with id {dev_id}')

    cfg = Config(id=dev_id, interval=interval, group=group)
    ConfigHandler.insert(cfg)

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
    app.logger.debug(f'device id -> {dev_id}')

    if not validate_field('id', dev_id):
        abort(400, 'Bad request')

    cfg = ConfigHandler.get(dev_id)
    if not cfg:
        app.logger.debug(f'config for {dev_id} not found')
        abort(404, "The device has no configuration")

    app.logger.debug(f'config data -> {cfg}')

    return jsonify(cfg), 200


@device_cfg_bp.route('/config/', methods=['GET'])
@jwt_required()
def get_configs():
    '''
    GET /devices/config endpoint implementation.

    :returns: On success, all the device configurations; otherwise an empty
              reply.

    '''
    cfgs = ConfigHandler.get_all()

    app.logger.debug(f'found cfgs -> {cfgs}')

    return jsonify(cfgs), 200


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

    if not ConfigHandler.entry_exists(dev_id):
        app.logger.debug(f'device {dev_id} has no config')
        abort(404, "There's no config for the specific device")

    app.logger.debug(f'found config for device {dev_id}')

    ConfigHandler.delete(dev_id)

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

    if not ConfigHandler.entry_exists(dev_id):
        app.logger.debug(f'device {dev_id} has no config')
        abort(404, "There's no config for the specific device")

    app.logger.debug(f'found config for device {dev_id}')

    ConfigHandler.update(dev_id, param, val)

    return jsonify({ 'msg': 'Config updated in database' }), 200
