from flask import jsonify
from requests import HTTPError, JSONDecodeError

from app.exceptions import ValidationError
from . import api


def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


@api.errorhandler(HTTPError)
def http_error(error):
    if error.response.status_code == 404:
        return not_found('The downstream service did not find what was requested')
    return internal_server_error('The downstream service had an error')


@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])


@api.errorhandler(KeyError)
def key_error(e):
    return internal_server_error('Key not found')


@api.errorhandler(JSONDecodeError)
def json_decode_error(e):
    return internal_server_error('Error occurred while attempting to decode json')


@api.errorhandler(404)
def not_found(error):
    response = jsonify({'error': 'not found', 'message': error})
    response.status_code = 404
    return response


@api.errorhandler(500)
def internal_server_error(error):
    response = jsonify({'error': 'internal server error', 'message': error})
    response.status_code = 500
    return response
