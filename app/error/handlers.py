from flask import jsonify

def bad_request(e):
    return jsonify({ 'msg': e.description }), 400

def resource_not_found(e):
    return jsonify({ 'msg': e.description }), 404

def internal_error(e):
    return jsonify({ 'msg': e.description }), 500

def unauthorized_error(e):
    return jsonify({ 'msg': e.description }), 401
