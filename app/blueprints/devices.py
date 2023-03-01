from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required

from app.storage.devices import Devices
from app.storage.models.device import Device
from app.validators import *

devices_bp = Blueprint('devices', __name__, url_prefix='/devices')

@devices_bp.route('/', methods=['POST'])
@jwt_required()
def register_device():
    # TODO: check if device already exists
    # TODO: check parameters
    dev = Device(
        id=request.json.get('device-id'),
        serial=request.json.get('serial-number'),
        group=request.json.get('group'),
        desc=request.json.get('description')
    )

    if not dev.id or not dev.serial or not dev.group:
        abort(400, 'bad request!')

    db = Devices()
    db.add(dev)

    return jsonify({ 'msg': 'device registered with success!' }), 201
#   serial = request.json.get('serial-number')
#   model = request.json.get('device-model')

#   if (not is_serial_valid(serial)) or (not is_model_valid(model)):
#       abort(400, 'Bad request')

#   # TODO: handle the errors properly
#   if cntrl.register(serial, model) != StatusCode.SUCCESS:
#       abort(500, '')

#   return jsonify({ 'msg': 'Device registered with success' }), 201

@devices_bp.route('/', methods=['GET'])
@jwt_required()
def get_devices():
    db = Devices()
    devices = db.get_all()

    return jsonify(devices), 200
#   devices = cntrl.get_all()

#   return jsonify(devices), 200

@devices_bp.route('/<string:dev_id>', methods=['GET'])
@jwt_required()
def get_device(dev_id):
    # TODO: check parameters

    if not dev_id:
        abort(400, 'bad request!')

    db = Devices()
    device = db.get(dev_id)

    if device:
        return jsonify(device), 200
    else:
        abort(404, "the device isn't registered on database!")
#   if not is_id_valid(dev_id):
#       abort(400, 'Bad request')

#   device = cntrl.get(dev_id)
#   if not device:
#       abort(404, "the device isn't registered on database!")

#   return jsonify(device), 200

@devices_bp.route('/<string:dev_id>', methods=['DELETE'])
@jwt_required()
def del_device(dev_id):
    # TODO: check parameters

    if not dev_id:
        abort(400, 'bad request!')

    db = Devices()
    if not db.get(dev_id):
        abort(404, "the device isn't registered on database!")

    db.rm(dev_id)

    return jsonify({ 'msg': 'device unregistered from database!' }), 200
#   if not is_id_valid(dev_id):
#       abort(400, 'Bad request')

#   if cntrl.rm(dev_id) == StatusCode.DEVICE_DO_NOT_EXIST:
#       abort(404, "The device isn't registered on database")

#   return jsonify({ 'msg': 'Device unregistered from database' }), 200

@devices_bp.route('/<string:dev_id>', methods=['PUT'])
@jwt_required()
def update_device(dev_id):
    # TODO: check parameters

    if not dev_id:
        abort(400, 'bad request!')

    db = Devices()
    if not db.get(dev_id):
        abort(404, "the device isn't registered on database!")

    db.update(dev_id, request.json.get('param'), request.json.get('value'))

    return jsonify({ 'msg': 'device updated in database!' }), 200
#   if not is_id_valid(dev_id):
#       abort(400, 'Bad request')

#   param = request.json.get('param')
#   val = request.json.get('value')

#   if cntrl.update(dev_id, param, val) == StatusCode.DEVICE_DO_NOT_EXIST:
#       abort(404, "The device isn't registered on database")

#   return jsonify({ 'msg': 'Device updated in database' }), 200
