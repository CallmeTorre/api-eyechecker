from os import getenv
from traceback import format_exc

from flask.views import MethodView
from flask import (Flask,
                   jsonify,
                   make_response,
                   request)

from eyechecker.utils.validation import validate_params
from eyechecker.utils.schemas import newpatientschema
from eyechecker.utils.command import Command

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

class NewPacient(MethodView):
    """
    Class that manages the creation of a new pacient.
    """

    decorators = [validate_params(newpatientschema)]
    def post(self, params):
        command = Command(params)
        command.execute("newpatientresponse")
        return make_response(
            jsonify(command.result),
            command.status)


new_patient_view = NewPacient.as_view('newpatient')

application.add_url_rule(
    '/patient/new',
    view_func=new_patient_view,
    methods=[
        'POST',
    ]
)

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