from models.database_mgr import DatabaseMgr
from models.entities.config import Config
from models.table_handler import TableHandler


class ConfigHandler(TableHandler):

    """Docstring for ConfigHandler. """

    @staticmethod
    def insert(entry):
        pass

    @staticmethod
    def delete(entry_id):
        pass

    @staticmethod
    def update(entry_id, key, value):
        pass

    @staticmethod
    def get_all(self):
        db = DatabaseMgr.get_db()
        cfgs = []

        with db.cursor() as cursor:
            cursor.execute('select * from configs')

            ret = cursor.fetchall()
            for i in ret:
                cfg = Config(id=ret[1], interval=ret[3], group=ret[2])
                cfgs.append(cfg)

        return cfgs

    @staticmethod
    def get(entry_id):
        db = DatabaseMgr.get_db()

        with db.cursor() as cursor:
            cursor.execute(f'select * from configs where dev_id = {entry_id}')

            ret = cursor.fetchone()
            if not ret:
                return None

        return Config(id=ret[1], interval=ret[3], group=ret[2])
