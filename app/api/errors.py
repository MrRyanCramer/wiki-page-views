from flask import jsonify, request
from app.exceptions import ValidationError
from . import api


def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])


@api.errorhandler(404)
def not_found(e):
    response = jsonify({'error': 'not found'})
    response.status_code = 404
    return response
