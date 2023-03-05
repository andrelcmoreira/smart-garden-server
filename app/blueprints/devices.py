from flask import abort, current_app, jsonify, request, Blueprint
from flask_jwt_extended import jwt_required

from app.controllers.device import *
from app.validators import validate_request, validate_field

devices_bp = Blueprint('devices', __name__, url_prefix='/devices')

@devices_bp.route('/', methods=['POST'])
@jwt_required()
def register_device():
    current_app.logger.debug('request payload -> %s' % request.json)

    if not validate_request(request.json):
        abort(400, 'Bad request')

    try:
        serial = request.json['serial-number']
        model = request.json['model']
        desc = request.json['description']
    except KeyError as e:
        current_app.logger.debug('missing %s in request' % e)
        abort(400, 'Missing required data')

    dev_id = register(serial, model, desc)
    if not dev_id:
        abort(500, 'Failed to register the device into the database')

    return jsonify(
        {
            'msg': 'Device registered with success',
            'id': dev_id
        }
    ), 201

@devices_bp.route('/', methods=['GET'])
@jwt_required()
def get_devices():
    devices = get_all()

    return jsonify(devices), 200

@devices_bp.route('/<string:dev_id>', methods=['GET'])
@jwt_required()
def get_device(dev_id):
    current_app.logger.debug('device id -> %s' % dev_id)

    if not validate_field('id', dev_id):
        abort(400, 'Bad request')

    device = get(dev_id)
    if not device:
        abort(404, "The device isn't registered on database")

    return jsonify(device), 200

@devices_bp.route('/<string:dev_id>', methods=['DELETE'])
@jwt_required()
def del_device(dev_id):
    current_app.logger.debug('device id -> %s' % dev_id)

    if not validate_field('id', dev_id):
        abort(400, 'Bad request')

    if delete(dev_id):
        abort(404, "The device isn't registered on database")

    return jsonify({ 'msg': 'Device unregistered from database' }), 200

@devices_bp.route('/<string:dev_id>', methods=['PUT'])
@jwt_required()
def update_device(dev_id):
    current_app.logger.debug('device id -> %s' % dev_id)

    if not validate_field('id', dev_id):
        abort(400, 'Bad request')

    try:
        param = request.json['param']
        val = request.json['value']
    except KeyError as e:
        current_app.logger.debug('missing %s in request' % e)
        abort(400, 'Missing required data')

    if update(dev_id, param, val):
        abort(404, "The device isn't registered on database")

    return jsonify({ 'msg': 'Device updated in database' }), 200
