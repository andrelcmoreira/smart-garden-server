from flask import Blueprint, request

register_bp = Blueprint('register', __name__, url_prefix='/register')

@register_bp.route('/', methods=['POST'])
def register_device():
    # TODO: check user credentials
    # TODO: add device into db
    print(request.json)
    print(request.json['user'])
    print(request.json['token'])
    print(request.json['device-id'])
    print(request.json['serial-number'])
    print(request.json['description'])
    print(request.json['group'])
    return 'hello, from register!', 200
