from os import getenv
from traceback import format_exc

from flask import (Flask,
                   jsonify,
                   make_response,
                   request)

application = Flask(__name__)

if getenv('ENV_SELECTOR') == 'dev':
    logging.warn('Disabling cross-origin checking')
    from flask_cors import CORS
    CORS(application)

@application.route('/')
def root():
    return make_response(
        jsonify(
            {'status': 'ok'}), 200)

@application.errorhandler(500)
def internal_error(error):
    if getenv('ENV_SELECTOR') == 'dev':
        return make_response(
            jsonify({
                'error': str(error),
                'traceback': format_exc()
            }), 500)
    else:
        return make_response(
            jsonify({
                'error': 'An internal error occurred'
            }), 500)

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8080)