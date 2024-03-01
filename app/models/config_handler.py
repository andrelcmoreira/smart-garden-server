from models.database_mgr import DatabaseMgr
from models.entities.config import Config
from models.table_handler import TableHandler


class ConfigHandler(TableHandler):

    '''
    Handler for configs table.

    '''

    @staticmethod
    def insert(cfg):
        db = DatabaseMgr.get_db()

        with db.cursor() as cursor:
            cursor.execute(f'''
                insert into configs(dev_id, dev_group, dev_interval)
                values ("{cfg.id}", "{cfg.group}", "{cfg.interval}")''')
            db.commit()

    @staticmethod
    def delete(entry_id):
        db = DatabaseMgr.get_db()

        with db.cursor() as cursor:
            cursor.execute(f'delete from configs where dev_id = {entry_id}')
            db.commit()

    @staticmethod
    def update(entry_id, key, value):
        db = DatabaseMgr.get_db()

        with db.cursor() as cursor:
            cursor.execute(f'''
                           update configs set {key} = "{value}"
                           where dev_id = {entry_id}
                           ''')
            db.commit()

    @staticmethod
    def get_all():
        db = DatabaseMgr.get_db()
        cfgs = []

        with db.cursor() as cursor:
            cursor.execute('select * from configs')

            ret = cursor.fetchall()
            for i in ret:
                cfg = Config(id=i[1], interval=i[3], group=i[2])
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

    @staticmethod
    def entry_exists(entry_id):
        db = DatabaseMgr.get_db()

        with db.cursor() as cursor:
            cursor.execute(f'select id from configs where dev_id = {entry_id}')

            ret = cursor.fetchone()

            return True if ret else False
