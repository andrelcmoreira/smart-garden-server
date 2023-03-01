from re import search

def is_user_valid(user):
    if not isinstance(user, str) or len(user) == 0:
        return False

    ret = search('^\w+$', user)

    return True if ret else False

def is_password_valid(passwd):
    if not isinstance(passwd, str) or len(passwd) == 0:
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

def is_param_valid(param):
    pass

def is_value_valid(value):
    pass
