from flask import jsonify

def bad_request(e):
    return jsonify({ 'message': e.description }), 400

def resource_not_found(e):
    return jsonify({ 'message': e.description }), 404
