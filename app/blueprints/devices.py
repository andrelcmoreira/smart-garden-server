import random
from string import ascii_lowercase, digits

from flask import abort, jsonify, request, Blueprint
from flask import current_app as app
from flask_jwt_extended import jwt_required

from app.storage.models.device import Device
from app.validators import validate_request, validate_field
from . import DEVICES_DB

devices_bp = Blueprint('devices', __name__, url_prefix='/devices')

@devices_bp.route('/', methods=['POST'])
@jwt_required()
def register_device():
    '''
    TODO

    '''
    app.logger.debug(f'request payload -> {request.json}')

    if not validate_request(request.json):
        abort(400, 'Bad request')

    try:
        serial = request.json['serial-number']
        model = request.json['model']
    except KeyError as key:
        app.logger.debug(f'missing {key} in request')
        abort(400, 'Missing required data')

    dev_id = ''.join(random.sample(ascii_lowercase + digits, 8))
    if not dev_id:
        app.logger.debug('empty device id')
        abort(500, 'Failed to register the device into the database')

    dev = Device(
        id=dev_id,
        serial=serial,
        model=model,
        desc=request.json.get('description')
    )
    DEVICES_DB.add(dev)

    return jsonify(
        {
            'msg': 'Device registered with success',
            'id': dev_id
        }
    ), 201

@devices_bp.route('/', methods=['GET'])
@jwt_required()
def get_devices():
    '''
    TODO

    '''
    devices = DEVICES_DB.get_all()

    return jsonify(devices), 200

@devices_bp.route('/<string:dev_id>', methods=['GET'])
@jwt_required()
def get_device(dev_id):
    '''
    TODO

    '''
    app.logger.debug(f'device id -> {dev_id}')

    if not validate_field('id', dev_id):
        abort(400, 'Bad request')

    device = DEVICES_DB.get(dev_id)
    if not device:
        abort(404, "The device isn't registered on database")

    return jsonify(device), 200

@devices_bp.route('/<string:dev_id>', methods=['DELETE'])
@jwt_required()
def del_device(dev_id):
    '''
    TODO

    '''
    app.logger.debug(f'device id -> {dev_id}')

    if not validate_field('id', dev_id):
        abort(400, 'Bad request')

    if not DEVICES_DB.get(dev_id):
        app.logger.debug(f'device {dev_id} not found')
        abort(404, "The device isn't registered on database")

    DEVICES_DB.rm(dev_id)

    return jsonify({ 'msg': 'Device unregistered from database' }), 200

@devices_bp.route('/<string:dev_id>', methods=['PUT'])
@jwt_required()
def update_device(dev_id):
    '''
    TODO

    '''
    app.logger.debug(f'device id -> {dev_id}')

    if not validate_field('id', dev_id):
        abort(400, 'Bad request')

    try:
        param = request.json['param']
        val = request.json['value']
    except KeyError as key:
        app.logger.debug(f'missing {key} in request')
        abort(400, 'Missing required data')

    if not DEVICES_DB.get(dev_id):
        app.logger.debug(f'device {dev_id} not found')
        abort(404, "The device isn't registered on database")

    DEVICES_DB.update(dev_id, param, val)

    return jsonify({ 'msg': 'Device updated in database' }), 200
