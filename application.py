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
from eyechecker.utils.schemas import (patientschema,
                                      doctorschema,
                                      patientlistschema,
                                      resetpasswordschema,
                                      analysisschema,
                                      appointmentschema)

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
    def get(self, params):
        command = Command(params, 'doctor')
        command.execute("get")
        return make_response(
            jsonify(command.result),
            command.status)

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


class ResetDoctorPasswordView(MethodView):
    """
    Class that reset the doctor's password.
    """
    decorators = [validate_params(resetpasswordschema)]
    def put(self, params):
        command = Command(params, 'doctor')
        command.execute("reset_password")
        return make_response(
            jsonify(command.result),
            command.status)


class RecoverDoctorPasswordView(MethodView):
    """
    Class that recover the doctor's password.
    """
    decorators = [validate_params(resetpasswordschema)]
    def post(self, params):
        command = Command(params, 'doctor')
        command.execute("recover_password")
        return make_response(
            jsonify(command.result),
            command.status)


class NewPatientAnalysis(MethodView):
    """
    Class that creates a new analysis
    """
    decorators = [validate_params(analysisschema)]
    def post(self, params):
        command = Command(params, 'patient')
        command.execute("new_analysis")
        return make_response(
            jsonify(command.result),
            command.status)


class Appointment(MethodView):
    """
    Class that creates a new appointment.
    """
    decorators = [validate_params(appointmentschema)]
    def get(self, params):
        command = Command(params, 'patient')
        command.execute("list_appointments")
        return make_response(
            jsonify(command.result),
            command.status)

    def post(self, params):
        command = Command(params, 'patient')
        command.execute("new_appointment")
        return make_response(
            jsonify(command.result),
            command.status)

    def delete(self, params):
        command = Command(params, 'patient')
        command.execute("delete_appointment")
        return make_response(
            jsonify(command.result),
            command.status)


patient_view = PatientView.as_view('patientview')
doctor_view = DoctorView.as_view('doctorview')
patient_list_view = PatientListView.as_view('patientlistview')
reset_doctor_password_view = ResetDoctorPasswordView.as_view('resetdoctorpasswordview')
recover_doctor_password_view = RecoverDoctorPasswordView.as_view('recoverdoctorpasswordview')
new_patient_analysis_view = NewPatientAnalysis.as_view('newpatientanalysisview')
appointment_view = Appointment.as_view('appointmentview')

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
        'GET', 'POST', 'DELETE', 'PUT'
    ]
)
application.add_url_rule(
    '/patient/list',
    view_func=patient_list_view,
    methods=[
        'GET'
    ]
)
application.add_url_rule(
    '/account/password/reset',
    view_func=reset_doctor_password_view,
    methods=[
        'PUT'
    ]
)
application.add_url_rule(
    '/account/password/recover',
    view_func=recover_doctor_password_view,
    methods=[
        'POST'
    ]
)
application.add_url_rule(
    '/patient/analysis',
    view_func=new_patient_analysis_view,
    methods=[
        'POST'
    ]
)
application.add_url_rule(
    '/appointment',
    view_func=appointment_view,
    methods=[
        'GET', 'POST'
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