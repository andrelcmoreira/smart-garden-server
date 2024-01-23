from flask import abort, jsonify, request, Blueprint
from flask import current_app as app
from flask_jwt_extended import jwt_required

from models.config import Config
from validators import validate_request, validate_field

from . import db

device_cfg_bp = Blueprint('device_config', __name__, url_prefix='/devices')


@device_cfg_bp.route('/<string:dev_id>/config/', methods=['POST'])
@jwt_required()
def config_device(dev_id):
    '''
    POST /devices/<id>/login endpoint implementation.

    :dev_id: ID of device.

    :returns: On success, a success reply; otherwise the suitable error reply
              (see the API documentation for more informations).

    '''
    app.logger.debug(f'device id -> {dev_id}')
    app.logger.debug(f'request payload -> {request.json}')

    if (not validate_field('id', dev_id)) or \
        (not validate_request(request.json)):
        abort(400, 'Bad request')

    try:
        # mandatory parameters
        interval = request.json['interval']
    except KeyError as key:
        app.logger.debug(f'missing {key} in request')
        abort(400, 'Missing required data')

    group = request.json.get('group') # optional

    with db.cursor() as cursor:
        cursor.execute(f'select * from devices where id = {dev_id}')

        ret = cursor.fetchone()
        if not ret:
            app.logger.debug(f'device {dev_id} not found')
            abort(404, "The device isn't registered on database")

        app.logger.debug(f'found device -> {ret}')

        cursor.execute(f'insert into configs(dev_id, dev_group, dev_interval) \
                       values ("{dev_id}", "{group}", "{interval}")')
        db.commit()

    return jsonify({ 'msg': 'Configuration registered with success' }), 201


@device_cfg_bp.route('/<string:dev_id>/config/', methods=['GET'])
@jwt_required()
def get_config(dev_id):
    '''
    GET /devices/<id>/config endpoint implementation.

    :dev_id: ID of device.

    :returns: On success, the device configuration; otherwise the suitable error
              reply (see the API documentation for more informations).

    '''
    if (not validate_field('id', dev_id)):
        abort(400, 'Bad request')

    with db.cursor() as cursor:
        cursor.execute(f'select * from configs where dev_id = {dev_id}')

        ret = cursor.fetchone()
        if not ret:
            app.logger.debug(f'device {dev_id} has no config')
            abort(404, "The device has no configuration")

        app.logger.debug(f'found device -> {ret}')

    cfg = Config(id=ret[0], interval=ret[2], group=ret[3])

    return jsonify(cfg), 200


@device_cfg_bp.route('/config/', methods=['GET'])
@jwt_required()
def get_configs():
    '''
    GET /devices/config endpoint implementation.

    :returns: On success, all the device configurations; otherwise an empty
              reply.

    '''
    cfgs = []

    with db.cursor() as cursor:
        cursor.execute(f'select * from configs')

        ret = cursor.fetchall()
        for entry in ret:
            app.logger.debug(f'found config -> {entry}')

            cfg = Config(entry[0], entry[3], entry[2])
            cfgs.append(cfg)

    return jsonify(cfgs), 200


@device_cfg_bp.route('/<string:dev_id>/config/', methods=['DELETE'])
@jwt_required()
def del_config(dev_id):
    '''
    DELETE /devices/<id>/config endpoint implementation.

    :dev_id: ID of device.

    :returns: On success, a success reply; otherwise the suitable error reply
              (see the API documentation for more informations).

    '''
    app.logger.debug(f'device id -> {dev_id}')

    if not validate_field('id', dev_id):
        abort(400, 'Bad request')

    with db.cursor() as cursor:
        cursor.execute(f'select * from configs where dev_id = {dev_id}')

        ret = cursor.fetchone()
        if not ret:
            app.logger.debug(f'device {dev_id} has no config')
            abort(404, "The device has no configuration")

        app.logger.debug(f'found device -> {ret}')

        cursor.execute(f'delete from configs where dev_id = {dev_id}')
        db.commit()

    return jsonify({ 'msg': 'Config deleted from database' }), 200


@device_cfg_bp.route('/<string:dev_id>/config/', methods=['PUT'])
@jwt_required()
def update_config(dev_id):
    '''
    PUT /devices/<id>/config endpoint implementation.

    :dev_id: ID of device.

    :returns: On success, a success reply; otherwise the suitable error reply
              (see the API documentation for more informations).

    '''
    app.logger.debug(f'device id -> {dev_id}')

    if (not validate_field('id', dev_id)) or \
        (not validate_request(request.json)):
        abort(400, 'Bad request')

    try:
        # mandatory parameters
        param = request.json['param']
        val = request.json['value']
    except KeyError as key:
        app.logger.debug(f'missing {key} in request')
        abort(400, 'Missing required data')

    with db.cursor() as cursor:
        cursor.execute(f'select * from configs where dev_id = {dev_id}')

        ret = cursor.fetchone()
        if not ret:
            app.logger.debug(f'device {dev_id} has no config')
            abort(404, "There's no config for the specific device")

        app.logger.debug(f'found device -> {ret}')

        cursor.execute(f'update configs set {param} = "{val}" \
                       where dev_id = {dev_id}')
        db.commit()

    return jsonify({ 'msg': 'Config updated in database' }), 200
