from flask import Blueprint, request, jsonify

from .storage.devices import Devices
from .storage.models.device import Device

devices_bp = Blueprint('devices', __name__, url_prefix='/devices')

@devices_bp.route('/', methods=['POST'])
def register_device():
    # TODO: check user credentials
    # TODO: check if device already exists
    # TODO: check parameters
    dev = Device(
        dev_id=request.json['device-id'],
        serial=request.json['serial-number'],
        group=request.json['group'],
        desc=request.json['description']
    )

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
    db = Devices()
    device = db.get(dev_id)

    if device:
        return jsonify(device), 200
    else:
        return jsonify(
            {
                'message': "the device isn't registered on database!"
            }
        ), 404

