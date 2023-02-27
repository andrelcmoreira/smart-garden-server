from re import search

def is_user_valid(user):
    if len(user) == 0:
        return False

    ret = search('^\w+$', user)

    return True if ret else False

def is_password_valid(passwd):
    if len(passwd) == 0:
        return False

    ret = search('^[\w@#\$&\*\-!\?;:]+$', passwd)

    return True if ret else False

def is_serial_valid(serial):
    if len(serial) == 0:
        return False

    ret = search('^[A-Z\d\-]+$', serial)

    return True if ret else False

def is_model_valid(model):
    if len(model) == 0:
        return False

    ret = search('^[\w\-]+$', model)

    return True if ret else False

def is_id_valid(dev_id):
    if len(dev_id) == 0:
        return False

    ret = search('^[a-zA-Z\d]+$', dev_id)

    return True if ret else False
