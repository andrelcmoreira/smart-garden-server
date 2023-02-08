from flask import Blueprint, request, jsonify, abort

from .storage.devices import Devices
from .storage.models.device import Device

devices_bp = Blueprint('devices', __name__, url_prefix='/devices')

@devices_bp.route('/', methods=['POST'])
def register_device():
    # TODO: check user credentials
    # TODO: check if device already exists
    # TODO: check parameters
    dev = Device(
        id=request.json['device-id'],
        serial=request.json['serial-number'],
        group=request.json['group'],
        desc=request.json['description']
    )

    if not dev.id or not dev.serial or not dev.group:
        abort(400, 'bad request!')

    db = Devices()
    db.add(dev)

    return jsonify({ 'message': 'device registered with success!' }), 201

@devices_bp.route('/', methods=['GET'])
def get_devices():
    # TODO: check user credentials
    db = Devices()
    devices = db.get_all()

    return jsonify(devices), 200

@devices_bp.route('/<string:dev_id>', methods=['GET'])
def get_device(dev_id):
    # TODO: check user credentials
    # TODO: check parameters

    if not dev_id:
        abort(400, 'bad request!')

    db = Devices()
    device = db.get(dev_id)

    if device:
        return jsonify(device), 200
    else:
        abort(404, "the device isn't registered on database!")

@devices_bp.route('/<string:dev_id>', methods=['DELETE'])
def del_device(dev_id):
    # TODO: check user credentials
    # TODO: check parameters

    if not dev_id:
        abort(400, 'bad request!')

    db = Devices()
    if not db.get(dev_id):
        abort(404, "the device isn't registered on database!")

    db.rm(dev_id)

    return jsonify({ 'message': 'device unregistered from database!' }), 200

@devices_bp.route('/<string:dev_id>', methods=['PUT'])
def update_device(dev_id):
    # TODO: check user credentials
    # TODO: check parameters

    if not dev_id:
        abort(400, 'bad request!')

    db = Devices()
    if not db.get(dev_id):
        abort(404, "the device isn't registered on database!")

    db.update(dev_id, request.json['param'], request.json['value'])

    return jsonify({ 'message': 'device updated in database!' }), 200
