#from flask import Blueprint, request, jsonify, abort
#from flask_jwt_extended import jwt_required
#
#from app.storage.devices import Devices
#from app.storage.models.config import Config
#
#config_bp = Blueprint('config', __name__, url_prefix='/config')
#
#@config_bp.route('/<string:dev_id>', methods=['POST'])
#@jwt_required()
#def config_device(dev_id):
#    # TODO: check if device already exists
#    # TODO: check parameters
#    cfg = Config(
#        interval=request.json.get('interval'),
#    )
#
#    # TODO
#    #if not dev.id or not dev.serial or not dev.group:
#    #    abort(400, 'Bad request')
#
#    #db = Devices()
#    #db.add(dev)
#
#    #return jsonify({ 'msg': 'Device registered with success' }), 201
#
#@config_bp.route('/<string:dev_id>', methods=['GET'])
#@jwt_required()
#def get_device_config(dev_id):
#    #db = Devices()
#    #devices = db.get_all()
#
#    #return jsonify(devices), 200
#    # TODO
