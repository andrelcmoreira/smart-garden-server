from json import load, dump
from os.path import exists, getsize

class Db:

    """
    Database abstract class implementation.

    """

    def __init__(self, file):
        """
        Constructor.

        :file: Database file.

        """
        self.db_file = file

        if not exists(self.db_file):
            with open(self.db_file, 'w') as f:
                dump([], f)

    def add(self, entry):
        """
        Add a new entry into the database.

        :entry: New entry to be added.

        """
        with open(self.db_file, 'r+') as f:
            content = []
            if getsize(self.db_file):
                content = load(f)

                f.seek(0)
                f.truncate(0)

            content.append(entry.__dict__)
            dump(content, f)

    def rm(self, id):
        """
        Remove an existing entry from the database.

        :id: ID of the entry to be removed.

        """
        with open(self.db_file, 'r+') as f:
            content = load(f)

            new_content = [it for it in content if not it['id'] == id]

            f.seek(0)
            f.truncate(0)

            dump(new_content, f)

    def get(self, id):
        """
        Retrieve an existing entry from the database.

        :id: ID of the entry to be retrieved.

        :return: On success, the requested device data; otherwise an empty
                 dict.

        """
        with open(self.db_file, 'r') as f:
            content = load(f)

            for entry in content:
                if entry['id'] == id:
                    return entry

            return {}

    def get_all(self):
        """
        Retrieve all the registered entries from the database.

        :return: All registered devices.

        """
        with open(self.db_file, 'r') as f:
            content = load(f)

            return content

    def update(self, id, key, value):
        """
        Update an existing entry from the database.

        :id: ID of the entry to be updated.
        :key: Key of the parameter to be updated.
        :value: New value to be updated.

        """
        with open(self.db_file, 'r+') as f:
            content = load(f)

            for it in content:
                if it['id'] == id:
                    it[key] = value

            f.seek(0)
            f.truncate(0)

            dump(content, f)
