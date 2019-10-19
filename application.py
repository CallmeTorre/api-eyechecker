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
from eyechecker.utils.schemas import (patientschema, doctorschema, patientlistschema)

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


class PatientView(MethodView):
    """
    Class that manages the patients operations.
    """

    decorators = [validate_params(patientschema)]
    def get(self, params):
        command = Command(params, 'patient')
        command.execute("get")
        return make_response(
            jsonify(command.result),
            command.status)

    def post(self, params):
        command = Command(params, 'patient')
        command.execute("create")
        return make_response(
            jsonify(command.result),
            command.status)

    def delete(self, params):
        command = Command(params, 'patient')
        command.execute("delete")
        return make_response(
            jsonify(command.result),
            command.status)

    def put(self, params):
        command = Command(params, 'patient')
        command.execute("update")
        return make_response(
            jsonify(command.result),
            command.status)

class DoctorView(MethodView):
    """
    Class that manages the doctors operations.
    """

    decorators = [validate_params(doctorschema)]
    def post(self, params):
        command = Command(params, 'doctor')
        command.execute("create")
        return make_response(
            jsonify(command.result),
            command.status)

    def delete(self, params):
        command = Command(params, 'doctor')
        command.execute("delete")
        return make_response(
            jsonify(command.result),
            command.status)

    def put(self, params):
        command = Command(params, 'doctor')
        command.execute("update")
        return make_response(
            jsonify(command.result),
            command.status)


class PatientListView(MethodView):
    """
    Class that list all the patients
    """
    decorators = [validate_params(patientlistschema)]
    def get(self, params):
        command = Command(params, 'patient')
        command.execute("list")
        return make_response(
            jsonify(command.result),
            command.status)


patient_view = PatientView.as_view('patientview')
doctor_view = DoctorView.as_view('doctorview')
patient_list_view = PatientListView.as_view('patientlistview')


application.add_url_rule(
    '/patient',
    view_func=patient_view,
    methods=[
        'GET', 'POST', 'DELETE', 'PUT'
    ]
)
application.add_url_rule(
    '/doctor',
    view_func=doctor_view,
    methods=[
        'POST', 'DELETE', 'PUT'
    ]
)
application.add_url_rule(
    '/patient/list',
    view_func=patient_list_view,
    methods=[
        'GET'
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