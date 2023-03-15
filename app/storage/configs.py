from .db import Db

class Configs(Db):

    def __init__(self):
        super().__init__('data/configs.db')
