import logging
from os import getenv
from traceback import format_exc

from flask.views import MethodView
from flask import (Flask,
                   jsonify,
                   make_response,
                   request)

from configuration.config import load
load()
from eyechecker.utils.validation import validate_params
from eyechecker.utils.command import Command
from eyechecker.utils.schemas import (newpatientschema,
                                      patientindexschema)


application = Flask(__name__)

if getenv('ENV_SELECTOR') == 'development':
    logging.info('Disabling cross-origin checking')
    from flask_cors import CORS
    CORS(application)

@application.route('/')
def root():
    return make_response(
        jsonify(
            {'status': 'ok'}), 200)

class NewPatient(MethodView):
    """
    Class that manages the creation of a new patient.
    """

    decorators = [validate_params(newpatientschema)]
    def post(self, params):
        command = Command(params)
        command.execute("newpatientresponse")
        return make_response(
            jsonify(command.result),
            command.status)


class PatientIndex(MethodView):
    """
    Class that manages the index of all the patients.
    """

    decorators = [validate_params(patientindexschema)]
    def get(self, params):
        command = Command(params)
        command.execute("patientindexresponse")
        return make_response(
            jsonify(command.result),
            command.status)

new_patient_view = NewPatient.as_view('newpatient')
patient_index_view = PatientIndex.as_view('patientindex')

application.add_url_rule(
    '/patient/new',
    view_func=new_patient_view,
    methods=[
        'POST',
    ]
)

application.add_url_rule(
    '/patient/index',
    view_func=patient_index_view,
    methods=[
        'GET',
    ]
)

@application.errorhandler(500)
def internal_error(error):
    """
    Method that handle how the errors are showed.
    """
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