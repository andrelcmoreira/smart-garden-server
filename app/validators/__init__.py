from re import search

def __is_user_valid(user):
    ret = search('^\w+$', user)

    return True if ret else False

def __is_password_valid(passwd):
    ret = search('^[\w@#\$&\*\-!\?;:]+$', passwd)

    return True if ret else False

def __is_serial_valid(serial):
    ret = search('^[\w\-]+$', serial)

    return True if ret else False

def __is_model_valid(model):
    ret = search('^[\w\-]+$', model)

    return True if ret else False

def __is_id_valid(dev_id):
    ret = search('^[a-z\d]+$', dev_id)

    return True if ret else False

def __is_description_valid(desc):
    ret = search('^[a-zA-Z\d ]+$', desc)

    return True if ret else False

def __is_param_valid(param):
    pass

def __is_value_valid(value):
    pass

__VALIDATORS = [
    {
        'field': 'user',
        'required': True,
        'func': __is_user_valid
    },
    {
        'field': 'password',
        'required': True,
        'func': __is_password_valid
    },
    {
        'field': 'serial-number',
        'required': True,
        'func': __is_serial_valid
    },
    {
        'field': 'model',
        'required': True,
        'func': __is_model_valid
    },
    {
        'field': 'id',
        'required': True,
        'func': __is_id_valid
    },
    {
        'field': 'description',
        'required': False,
        'func': __is_description_valid
    },
    {
        'field': 'param',
        'required': True,
        'func': __is_param_valid
    },
    {
        'field': 'value',
        'required': True,
        'func': __is_value_valid
    }
]

def __get_validator(field):
    for entry in __VALIDATORS:
        if entry['field'] == field:
            return entry

    return None

def validate_request(req_json):
    for entry in req_json:
        validator_entry = __get_validator(entry)

        if not validator_entry:
            return False

        func = validator_entry['func']
        required = validator_entry['required']
        value = req_json.get(entry)

        if (len(value) == 0) and required:
            return False

        if not func(value):
            return False

    return True

def validate_field(field, value):
    validator = __get_validator(field)

    if not validator:
        return False

    return validator['func'](value)
