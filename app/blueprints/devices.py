from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required

from app.controllers.device import *
from app.validators import validate_request, validate_field

devices_bp = Blueprint('devices', __name__, url_prefix='/devices')

@devices_bp.route('/', methods=['POST'])
@jwt_required()
def register_device():
    if not validate_request(request.json):
        abort(400, 'Bad request')

    serial = request.json.get('serial-number')
    model = request.json.get('model')
    desc = request.json.get('description')

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
    if not validate_field('id', dev_id):
        abort(400, 'Bad request')

    device = get(dev_id)
    if not device:
        abort(404, "The device isn't registered on database")

    return jsonify(device), 200

@devices_bp.route('/<string:dev_id>', methods=['DELETE'])
@jwt_required()
def del_device(dev_id):
    if not validate_field('id', dev_id):
        abort(400, 'Bad request')

    if delete(dev_id):
        abort(404, "The device isn't registered on database")

    return jsonify({ 'msg': 'Device unregistered from database' }), 200

@devices_bp.route('/<string:dev_id>', methods=['PUT'])
@jwt_required()
def update_device(dev_id):
    if not validate_field('id', dev_id):
        abort(400, 'Bad request')

    param = request.json.get('param')
    val = request.json.get('value')

    if update(dev_id, param, val):
        abort(404, "The device isn't registered on database")

    return jsonify({ 'msg': 'Device updated in database' }), 200
