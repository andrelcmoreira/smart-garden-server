from .db import Db

from json import load, dump
from os.path import exists, getsize

class Devices(Db):

    def __init__(self):
        self.db_file = 'data/devices.db'

        if not exists(self.db_file):
            with open(self.db_file, 'w') as f:
                pass


    def add(self, entry):
        with open(self.db_file, 'r+') as f:
            content = []
            if getsize(self.db_file):
                content = load(f)

                f.seek(0)
                f.truncate(0)

            content.append(entry.__dict__)
            dump(content, f)

    def rm(self, entry):
        pass

    def update(self, entry):
        pass
