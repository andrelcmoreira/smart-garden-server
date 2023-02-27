from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required

from app.storage.devices import Devices
from app.storage.models.device import Device
from app.validators import *

devices_bp = Blueprint('devices', __name__, url_prefix='/devices')

@devices_bp.route('/', methods=['POST'])
@jwt_required()
def register_device():
    serial = request.json.get('serial-number')
    model = request.json.get('device-model')

    if (not is_serial_valid(serial)) or (not is_model_valid(model)):
        abort(400, 'Bad request')

    # TODO: handle the errors properly
    if cntrl.register(serial, model) != StatusCode.SUCCESS:
        abort(500, '')

    return jsonify({ 'msg': 'Device registered with success' }), 201

@devices_bp.route('/', methods=['GET'])
@jwt_required()
def get_devices():
    devices = cntrl.get_all()

    return jsonify(devices), 200

@devices_bp.route('/<string:dev_id>', methods=['GET'])
@jwt_required()
def get_device(dev_id):
    if not is_id_valid(dev_id):
        abort(400, 'Bad request')

    device = cntrl.get(dev_id)
    if not device:
        abort(404, "the device isn't registered on database!")

    return jsonify(device), 200

@devices_bp.route('/<string:dev_id>', methods=['DELETE'])
@jwt_required()
def del_device(dev_id):
    if not is_id_valid(dev_id):
        abort(400, 'Bad request')

    if cntrl.rm(dev_id) == StatusCode.DEVICE_DO_NOT_EXIST:
        abort(404, "The device isn't registered on database")

    return jsonify({ 'msg': 'Device unregistered from database' }), 200

@devices_bp.route('/<string:dev_id>', methods=['PUT'])
@jwt_required()
def update_device(dev_id):
    if not is_id_valid(dev_id):
        abort(400, 'Bad request')

    param = request.json.get('param')
    val = request.json.get('value')

    if cntrl.update(dev_id, param, val) == StatusCode.DEVICE_DO_NOT_EXIST:
        abort(404, "The device isn't registered on database")

    return jsonify({ 'msg': 'Device updated in database' }), 200
