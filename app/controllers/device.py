from app.storage.devices import Devices
from app.storage.models.device import Device

from random import sample
from string import ascii_lowercase, digits

__DB = Devices()

def register(serial, model, desc):
    # TODO: handle the errors properly
    dev_id = ''.join(sample(ascii_lowercase + digits, 8)) # TODO: remove this logic from here
    dev = Device(id=dev_id, serial=serial, model=model, desc=desc)

    __DB.add(dev)

    return dev_id

def get_all():
    return __DB.get_all()

def get(dev_id):
    return __DB.get(dev_id)

def delete(dev_id):
    if not __DB.get(dev_id):
        return 1

    __DB.rm(dev_id)

    return 0

def update(dev_id, param, value):
    if not __DB.get(dev_id):
        return 1

    __DB.update(dev_id, param, value)

    return 0
