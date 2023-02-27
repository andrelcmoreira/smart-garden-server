from .db import Db

from json import load, dump
from os.path import exists, getsize

class Devices(Db):

    def __init__(self):
        self.db_file = 'data/devices.db'

        if not exists(self.db_file):
            with open(self.db_file, 'w') as f:
                dump([], f)

    def add(self, entry):
        with open(self.db_file, 'r+') as f:
            content = []
            if getsize(self.db_file):
                content = load(f)

                f.seek(0)
                f.truncate(0)

            content.append(entry.__dict__)
            dump(content, f)

    def rm(self, id):
        with open(self.db_file, 'r+') as f:
            content = load(f)

            new_content = [it for it in content if not it['id'] == id]

            f.seek(0)
            f.truncate(0)

            dump(new_content, f)

    def get(self, id):
        with open(self.db_file, 'r') as f:
            content = load(f)

            for entry in content:
                if entry['id'] == id:
                    return entry

            return {}

    def get_all(self):
        with open(self.db_file, 'r') as f:
            content = load(f)

            return content

    def update(self, id, key, value):
        with open(self.db_file, 'r+') as f:
            content = load(f)

            for it in content:
                if it['id'] == id:
                    it[key] = value

            f.seek(0)
            f.truncate(0)

            dump(content, f)
