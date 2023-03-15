from re import search

__VALIDATORS = [
    {
        'field': 'user',
        'required': True,
        'pattern': '^\w+$'
    },
    {
        'field': 'password',
        'required': True,
        'pattern': '^[\w@#\$&\*\-!\?;:]+$'
    },
    {
        'field': 'serial-number',
        'required': True,
        'pattern': '^[\w\-]+$'
    },
    {
        'field': 'model',
        'required': True,
        'pattern': '^[\w\-]+$'
    },
    {
        'field': 'id',
        'required': True,
        'pattern': '^[a-z\d]+$'
    },
    {
        'field': 'description',
        'required': False,
        'pattern': '^[a-zA-Z\d ]+$'
    },
    {
        'field': 'group',
        'required': False,
        'pattern': '^[a-zA-Z\d ]+$'
    },
    {
        'field': 'param',
        'required': True,
        'pattern': '^[a-z_\-]+$'
    },
    {
        'field': 'value',
        'required': True,
        'pattern': '^[\w@#\$&\*\-!\?;:]+$'
    }
]

def __get_validator(field):
    for entry in __VALIDATORS:
        if entry['field'] == field:
            return entry

    return None

def validate_field(field, value):
    validator = __get_validator(field)

    if not validator:
        return False

    pattern = validator['pattern']
    required = validator['required']

    if len(value):
        ret = search(pattern, value)
        if (not ret) and required:
            return False
    elif required:
        return False

    return True

def validate_request(req_json):
    if not req_json:
        return False

    for field in req_json:
        value = req_json.get(field)
        if not validate_field(field, value):
            return False

    return True
