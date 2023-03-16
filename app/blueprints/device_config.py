from flask import abort, jsonify, request, Blueprint
from flask import current_app as app
from flask_jwt_extended import jwt_required

from app.storage.models.config import Config
from app.validators import validate_request, validate_field
from . import CONFIGS_DB

device_cfg_bp = Blueprint('device_config', __name__,
                          url_prefix='/devices/<string:dev_id>/config')

@device_cfg_bp.route('/', methods=['POST'])
@jwt_required()
def config_device(dev_id):
    '''
    TODO

    '''
    app.logger.debug(f'device id -> {dev_id}')
    app.logger.debug(f'request payload -> {request.json}')

    if (not validate_field('id', dev_id)) or \
        (not validate_request(request.json)):
        abort(400, 'Bad request')

    try:
        interval = request.json['interval']
    except KeyError as key:
        app.logger.debug(f'missing {key} in request')
        abort(400, 'Missing required data')

    cfg = Config(id=dev_id, group=request.json.get('group'), interval=interval)

    CONFIGS_DB.add(cfg)

    return jsonify({ 'msg': 'Configuration registered with success' }), 201

@device_cfg_bp.route('/', methods=['GET'])
@jwt_required()
def get_config(dev_id):
    '''
    TODO

    '''
    if (not validate_field('id', dev_id)):
        abort(400, 'Bad request')

    config = CONFIGS_DB.get(dev_id)

    return jsonify(config), 200
