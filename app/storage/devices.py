from .db import Db

class Devices(Db):

    """
    Devices database implementation.

    """
    def __init__(self):
        """
        Constructor.

        """
        super().__init__('data/devices.db')
