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
                                      appointmentschema,
                                      loginschema,
                                      listanalysisschema,
                                      getanalysisschema)

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

    def put(self, params):
        command = Command(params, 'patient')
        command.execute("update_appointment")
        return make_response(
            jsonify(command.result),
            command.status)

class Login(MethodView):
    """
    Class that creates a new appointment.
    """
    decorators = [validate_params(loginschema)]
    def post(self, params):
        command = Command(params, 'doctor')
        command.execute("validate_login")
        return make_response(
            jsonify(command.result),
            command.status)

class ListCatalogueEstadoCivil(MethodView):
    """
    Class that list estado civil catalogue info.
    """
    def get(self):
        command = Command({}, 'patient')
        command.execute("list_catalogue_estado_civil")
        return make_response(
            jsonify(command.result),
            command.status)

class ListCatalogueOcupacion(MethodView):
    """
    Class that list estado civil catalogue info.
    """
    def get(self):
        command = Command({}, 'patient')
        command.execute("list_catalogue_ocupacion")
        return make_response(
            jsonify(command.result),
            command.status)

class ListCatalogueEstadoCita(MethodView):
    """
    Class that list estado civil catalogue info.
    """
    def get(self):
        command = Command({}, 'patient')
        command.execute("list_catalogue_estado_cita")
        return make_response(
            jsonify(command.result),
            command.status)

class ListPatientAnalysis(MethodView):
    """
    Class that list patient analysis info.
    """
    decorators = [validate_params(listanalysisschema)]
    def get(self, params):
        command = Command(params, 'patient')
        command.execute("list_analysis")
        return make_response(
            jsonify(command.result),
            command.status)

#class GetPatientAnalysis(MethodView):
    """
    Class that get patient analysis info.
    """
#    decorators = [validate_params(getanalysisschema)]
#    def get(self, params):
#        command = Command(params, 'patient')
#        command.execute("get_analysis")
#        return make_response(
#            jsonify(command.result),
#            command.status)

patient_view = PatientView.as_view('patientview')
doctor_view = DoctorView.as_view('doctorview')
patient_list_view = PatientListView.as_view('patientlistview')
reset_doctor_password_view = ResetDoctorPasswordView.as_view('resetdoctorpasswordview')
recover_doctor_password_view = RecoverDoctorPasswordView.as_view('recoverdoctorpasswordview')
new_patient_analysis_view = NewPatientAnalysis.as_view('newpatientanalysisview')
appointment_view = Appointment.as_view('appointmentview')
validate_login_view = Login.as_view('loginview')
list_catalogue_estado_civil_view = ListCatalogueEstadoCivil.as_view('listcatalogueestadocivil')
list_catalogue_ocupacion_view = ListCatalogueOcupacion.as_view('listcatalogueocupacion')
list_catalogue_estado_cita_view = ListCatalogueEstadoCita.as_view('listacatalogueestadocita')
list_patient_analysis_view = ListPatientAnalysis.as_view('listpatientanalysisview')
#get_patient_analysis_view = GetPatientAnalysis.as_view('getpatientanalysisview')

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
        'GET', 'POST', 'DELETE', 'PUT'
    ]
)
application.add_url_rule(
    '/login',
    view_func=validate_login_view,
    methods=[
        'POST'
    ]
)
application.add_url_rule(
    '/list/catalogue/estado_civil',
    view_func=list_catalogue_estado_civil_view,
    methods=[
        'GET'
    ]
)
application.add_url_rule(
    '/list/catalogue/ocupacion',
    view_func=list_catalogue_ocupacion_view,
    methods=[
        'GET'
    ]
)
application.add_url_rule(
    '/list/catalogue/estado_cita',
    view_func=list_catalogue_estado_cita_view,
    methods=[
        'GET'
    ]
)
application.add_url_rule(
    '/patient/analysis/list',
    view_func=list_patient_analysis_view,
    methods=[
        'GET'
    ]
)
#application.add_url_rule(
#    '/patient/analysis/get',
#    view_func=get_patient_analysis_view,
#    methods=[
#        'GET'
#    ]
#)
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