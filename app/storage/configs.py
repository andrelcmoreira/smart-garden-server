from .db import Db

class Configs(Db):

    """
    Configurations database implementation.

    """

    def __init__(self):
        """
        Constructor.

        """
        super().__init__('data/configs.db')
