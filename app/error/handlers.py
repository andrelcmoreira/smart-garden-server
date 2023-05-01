from flask import jsonify

def bad_request(e):
    """
    Error handler for error code 400.

    :e: The exception instance.

    :return: The formatted error reply.

    """
    return jsonify({ 'msg': e.description }), 400

def resource_not_found(e):
    """
    Error handler for error code 404.

    :e: The exception instance.

    :return: The formatted error reply.

    """
    return jsonify({ 'msg': e.description }), 404

def internal_error(e):
    """
    Error handler for error code 500.

    :e: The exception instance.

    :return: The formatted error reply.

    """
    return jsonify({ 'msg': e.description }), 500

def unauthorized_error(e):
    """
    Error handler for error code 401.

    :e: The exception instance.

    :return: The formatted error reply.

    """
    return jsonify({ 'msg': e.description }), 401
