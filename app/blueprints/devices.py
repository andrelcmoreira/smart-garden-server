from flask import abort, jsonify, request, Blueprint
from flask import current_app as app
from flask_jwt_extended import jwt_required

from models.entities.device import Device
from models.device_handler import *
from validators import validate_request, validate_field


devices_bp = Blueprint('devices', __name__, url_prefix='/devices')


@devices_bp.route('/', methods=['POST'])
@jwt_required()
def register_device():
    '''
    POST /devices endpoint implementation.

    :returns: On success, a success reply, and the device's ID; otherwise the
              suitable error reply (see the API documentation for more
              informations).

    '''
    app.logger.debug(f'request payload -> {request.json}')

    if not validate_request(request.json):
        abort(400, 'Bad request')

    try:
        # mandatory parameters
        serial = request.json['serial-number']
        model = request.json['model']
    except KeyError as key:
        app.logger.debug(f'missing {key} in request')
        abort(400, 'Missing required data')

    desc = request.json.get('description') # optional

    dev_data = Device(serial=serial, model=model, desc=desc)
    reg_id = add_device(dev_data)

    return jsonify(
        {
            'msg': 'Device registered with success',
            'id': reg_id
        }
    ), 201


@devices_bp.route('/', methods=['GET'])
@jwt_required()
def get_devices():
    '''
    GET /devices endpoint implementation.

    :returns: On success, all registered devices; otherwise an empty reply.

    '''
    devices = get_all_devices()

    app.logger.debug(f'found devices -> {devices}')

    return jsonify(devices), 200


@devices_bp.route('/<string:dev_id>', methods=['GET'])
@jwt_required()
def get_device(dev_id):
    '''
    GET /devices/<id> endpoint implementation.

    :dev_id: ID of device.

    :returns: On success, the device information; otherwise the suitable error
              reply (see the API documentation for more informations).

    '''
    app.logger.debug(f'device id -> {dev_id}')

    if not validate_field('id', dev_id):
        abort(400, 'Bad request')

    dev = get_device_with_id(dev_id)
    if not dev:
        abort(404, "The device isn't registered on database")

    app.logger.debug(f'device data -> {ret}')

    return jsonify(dev), 200


@devices_bp.route('/<string:dev_id>', methods=['DELETE'])
@jwt_required()
def del_device(dev_id):
    '''
    DELETE /devices/<id> endpoint implementation.

    :dev_id: ID of device.

    :returns: On success, a success reply; otherwise the suitable error reply
              (see the API documentation for more informations).

    '''
    app.logger.debug(f'device id -> {dev_id}')

    if not validate_field('id', dev_id):
        abort(400, 'Bad request')

    if not device_exists(dev_id):
        app.logger.debug(f'device {dev_id} not found')
        abort(404, "The device isn't registered on database")

    app.logger.debug(f'found device with id {dev_id}')

    rm_device_with_id(dev_id)

    return jsonify({ 'msg': 'Device unregistered from database' }), 200


@devices_bp.route('/<string:dev_id>', methods=['PUT'])
@jwt_required()
def update_device(dev_id):
    '''
    PUT /devices/<id> endpoint implementation.

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

    if not device_exists(dev_id):
        app.logger.debug(f'device {dev_id} not found')
        abort(404, "The device isn't registered on database")

    app.logger.debug(f'found device with id {dev_id}')

    update_device_with_id(dev_id, param, value)

    return jsonify({ 'msg': 'Device updated in database' }), 200
