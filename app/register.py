from flask import Blueprint, request

from .storage.devices import Devices
from .storage.models.device import Device

register_bp = Blueprint('register', __name__, url_prefix='/register')

@register_bp.route('/', methods=['POST'])
def register_device():
    # TODO: check user credentials
    # TODO: check if device already exists
    dev = Device(
        dev_id=request.json['device-id'],
        serial=request.json['serial-number'],
        group=request.json['group'],
        desc=request.json['description']
    )

    db = Devices()
    db.add(dev)

    return 'device registered with success!\n', 201
