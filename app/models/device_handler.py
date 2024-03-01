from models.database_mgr import DatabaseMgr
from models.entities.device import Device
from models.table_handler import TableHandler


class DeviceHandler(TableHandler):

    '''
    Handler for devices table.

    '''

    @staticmethod
    def insert(entry):
        db = DatabaseMgr.get_db()

        with db.cursor() as c:
            c.execute(f'''
                      insert into devices(serial, model, description)
                      values ("{entry.serial}", "{entry.model}", "{entry.desc}")
                      ''')
            db.commit()

            # get the device ID
            c.execute('select max(id) from devices') # TODO: improve this

            return c.fetchone()

    @staticmethod
    def delete(entry_id):
        db = DatabaseMgr.get_db()

        with db.cursor() as cursor:
            cursor.execute(f'delete from devices where id = {entry_id}')
            db.commit()

    @staticmethod
    def update(entry_id, key, value):
        db = DatabaseMgr.get_db()

        with db.cursor() as cursor:
            cursor.execute(f'''
                           update devices set {key} = "{value}"
                           where id = {entry_id}
                           ''')
            db.commit()

    @staticmethod
    def get_all():
        db = DatabaseMgr.get_db()
        devices = []

        with db.cursor() as cursor:
            cursor.execute('select * from devices')

            ret = cursor.fetchall()
            for i in ret:
                dev = Device(id=i[0], serial=i[1], model=i[2], desc=i[3])
                devices.append(dev)

        return devices

    @staticmethod
    def get(entry_id):
        db = DatabaseMgr.get_db()

        with db.cursor() as cursor:
            cursor.execute(f'select * from devices where id = {entry_id}')

            ret = cursor.fetchone()
            if not ret:
                return None

        return Device(id=ret[0], serial=ret[1], model=ret[2], desc=ret[3])

    @staticmethod
    def entry_exists(entry_id):
        db = DatabaseMgr.get_db()

        with db.cursor() as cursor:
            cursor.execute(f'select id from devices where id = {entry_id}')

            ret = cursor.fetchone()

            return bool(ret)
