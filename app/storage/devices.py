from .db import Db

class Devices(Db):

    def __init__(self):
        super().__init__('data/devices.db')
