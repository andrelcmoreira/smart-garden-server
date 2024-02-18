from models.entities.device import Device


def add_device(data):
    with db.cursor() as cursor:
        cursor.execute(f'insert into devices(serial, model, description) \
                       values ("{data.serial}", "{data.model}", "{data.desc}")')
        db.commit()

        # get the device ID
        cursor.execute('select max(id) from devices') # TODO: improve this
        return cursor.fetchone()


def rm_device_with_id(dev_id):
    #with app.db.cursor() as cursor:
    #    cursor.execute(f'select * from devices where id = {dev_id}')

    #    ret = cursor.fetchone()
    #    if not ret:
    #        app.logger.debug(f'device {dev_id} not found')
    #        abort(404, "The device isn't registered on database")

    #    app.logger.debug(f'found device -> {ret}')

    #    cursor.execute(f'delete from devices where id = {dev_id}')
    #    app.db.commit()


def update_device(data):
#    with app.db.cursor() as cursor:
#        cursor.execute(f'select * from devices where id = {dev_id}')
#
#        ret = cursor.fetchone()
#        if not ret:
#            app.logger.debug(f'device {dev_id} not found')
#            abort(404, "The device isn't registered on database")
#
#        app.logger.debug(f'found device -> {ret}')
#
#        cursor.execute(f'update devices set {param} = "{val}" \
#                       where id = {dev_id}')
#        app.db.commit()
#
    pass


def get_device_with_id(dev_id):
    with db.cursor() as cursor:
        cursor.execute(f'select * from devices where id = {dev_id}')

        ret = cursor.fetchone()
        if not ret:
            return None

    return Device(id=ret[0], serial=ret[1], model=ret[2], desc=ret[3])


def get_all_devices(db):
    devices = []

    with db.cursor() as cursor:
        cursor.execute('select * from devices')

        ret = cursor.fetchall()
        for i in ret:
            dev = Device(id=i[0], serial=i[1], model=i[2], desc=i[3])
            devices.append(dev)

    return devices
