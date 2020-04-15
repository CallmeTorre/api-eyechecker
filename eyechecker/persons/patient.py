import logging

from sqlalchemy import Table, cast, desc
from sqlalchemy.sql import select, and_
from sqlalchemy.types import String, Date

from eyechecker.persons.person import Person
from eyechecker.utils.formatter import format_patient, format_appointments, format_analysis
from eyechecker.utils.helpers import save_temp_image, image_analysis
from eyechecker.utils.pdf import create_pdf, get_pdf_url
class Patient(Person):
    """
    Class that defines main patient's operations.
    """
    def __init__(self, params):
        """
        Patient's constructor method.
        """
        super().__init__(params)
        self._table = Table(
            'pacientes',
            self.meta,
            autoload=True,
            autoload_with=self.engine)

    @property
    def table(self):
        """
        Patient's table.
        """
        return self._table

    #@classmethod
    def create(self):
        """
        Method that creates a new patient in the database.
        """
        transaction = self._connection.begin()
        self._params['id_persona'] = self._insert_person()
        patient = format_patient(self._params)
        try:
            id = self._connection.execute(
                self.table.insert().values(**patient)).inserted_primary_key[0]
            transaction.commit()
            return {'id_paciente': id,
                    'id_persona': self._params['id_persona']}, 201
        except Exception as e:
            logging.error("No se puedo crear el paciente")
            logging.exception(str(e))
            transaction.rollback()
            return {'error': "No se puedo crear el paciente"}, 500

    #@classmethod
    def delete(self):
        """
        Method that deletes a patient.
        """
        transaction = self._connection.begin()
        try:
            self._connection.execute(
                self.persons.delete().\
                where(self.persons.c.id == self._params['id']))
            transaction.commit()
            return {'status': 'Paciente borrado correctamente'}, 200
        except Exception as e:
            logging.error("No se puedo borrar el paciente")
            logging.exception(str(e))
            transaction.rollback()
            return {'error': "No se puedo borrar el paciente"}, 500

    #@classmethod
    def update(self):
        """
        Method that updates the information of a patient.
        """
        transaction = self._connection.begin()
        try:
            self._connection.execute(
                self.table.update().\
                where(self.table.c.id == self._params['id']).\
                values(**self._params))
            transaction.commit()
            return {'status': 'Paciente actualizado correctamente'}, 200
        except Exception as e:
            logging.error("No se puedo actualizar el paciente")
            logging.exception(str(e))
            transaction.rollback()
            return {'error': "No se puedo actualizar el paciente"}, 500

    def patient_list_filters(self):
        """
        Method that creates the filters depending on the params.
        """
        filters = []
        if self._params['nombre'] != 'all':
            like_string = '%' + self._params['nombre'] + '%'
            filters.append(self.persons.c.nombre.ilike(like_string))
            return filters

        if self._params['curp'] != 'all':
            like_string = '%' + self._params['curp'] + '%'
            filters.append(self.table.c.curp.ilike(like_string))
            return filters

        return filters

    def list(self):
        """
        Method that list the information of all the patients.
        """
        result = []
        patients_list = self.engine.execute(
                            select([
                                self.persons.c.id.label('id_persona'),
                                self.table.c.id.label('id_paciente'),
                                self.table.c.curp,
                                (cast(self.persons.c.nombre, String) + " " + \
                                 cast(self.persons.c.apellido_paterno, String) + " " + \
                                 cast(self.persons.c.apellido_materno, String)).label('nombre'),
                                self.persons.c.fecha_nacimiento,
                                self.persons.c.telefono_celular,
                                self.persons.c.email]).\
                            select_from(self.table.\
                                outerjoin(
                                    self.persons,
                                    self.persons.c.id ==
                                    self.table.c.id_persona)).\
                            where(
                                and_(
                                    *self.patient_list_filters())).\
                            order_by(desc('nombre'))).fetchall()
        for patient in patients_list:
            result.append({
                'id_persona': patient.id_persona,
                'id_paciente': patient.id_paciente,
                'nombre': patient.nombre,
                'curp': patient.curp,
                'fecha_nacimiento': patient.fecha_nacimiento.strftime("%d-%m-%Y"),
                'telefono_celular': patient.telefono_celular,
                'email': patient.email
            })
        return result, 200

    def get(self):
        """
        Method that retrieves the information of a patient.
        """
        patient_info = self.engine.execute(
                            select([
                                self.persons,
                                self.table,
                                self.table.c.id.label('id_paciente'),
                                self.cat_estado_civil.c.tipo.label('estado_civil'),
                                self.cat_ocupacion.c.ocupacion]).\
                            select_from(self.table.\
                                outerjoin(
                                    self.persons,
                                    self.persons.c.id ==
                                    self.table.c.id_persona).\
                                outerjoin(
                                    self.cat_ocupacion,
                                    self.cat_ocupacion.c.id ==
                                    self.table.c.id_ocupacion).\
                                outerjoin(
                                    self.cat_estado_civil,
                                    self._cat_estado_civil.c.id ==
                                    self.table.c.id_estado_civil)).\
                            where(self.persons.c.id == self._params['id'])).fetchone()
        return {
            'id_paciente': patient_info.id_paciente,
            'nombre': patient_info.nombre + " " + patient_info.apellido_paterno + " " + patient_info.apellido_materno,
            'fecha_nacimiento': patient_info.fecha_nacimiento,
            'email': patient_info.email,
            'telefono_celular': patient_info.telefono_celular,
            'genero': patient_info.genero,
            'curp': patient_info.curp,
            'ocupacion': patient_info.ocupacion,
            'estado_civil': patient_info.estado_civil,
            'enfermedades_cronicas': patient_info.enfermedades_cronicas,
            'enfermedades_recientes': patient_info.enfermedades_recientes,
            'medicamentos': patient_info.medicamentos,
            'enfermedades_hereditarias': patient_info.enfermedades_hereditarias
        }, 200

    def new_analysis(self):
        #TODO Rewrite this method.
        """
        Method that receives the patient eye image(s) and create the analysis.
        """
        #TODO Make a better validation for the parameters.
        result = {}
        patient_info , _ = self.get()
        for eye in ['left_eye', 'right_eye']:
            result.update(image_analysis(eye, self._params))
        pdf_path = create_pdf(result, patient_info)
        reporte_info = {
            'id_paciente': patient_info['id_paciente'],
            'id_doctor': self._params['id_medico'],
            'url_reporte': pdf_path
        }
        id_reporte = self.engine.execute(
                self.reportes.insert().values(**reporte_info)).inserted_primary_key[0]
        return {'pdf_path': pdf_path,
                'id_reporte': id_reporte}, 200

    def _check_appointment_availability_filters(self):
        """
        Private method that work as filters to check if a date is open.
        """
        filters = []

        filters.append(self._params['id_doctor'] == self.citas.c.id_doctor)

        filters.append(self._params['fecha_agendada'] == self.citas.c.fecha_agendada)

        return filters

    def _check_appointment_availability(self):
        """
        Method that checks if the doctor doesn't have an appointment
        at the same time.
        """
        availability = self._connection.execute(
            select([
                self.citas]).\
            where(
                and_(
                    *self._check_appointment_availability_filters()))).fetchone()
        return True if availability is None else False

    def new_appointment(self):
        """
        Method that receives the information of an appointment and creates one.
        """
        transaction = self._connection.begin()
        try:
            if self._check_appointment_availability() is True:
                self._connection.execute(
                    self.citas.insert().values(**self._params))
                transaction.commit()
                return {'status': 'Cita creada correctamente'}, 201
            else:
                return {'status': 'Horario ocupado'}, 200
        except Exception as e:
            logging.error("No se puedo crear la cita")
            logging.exception(str(e))
            transaction.rollback()
            return {'error': "No se puedo crear la cita"}, 500

    def patient_citas_filters(self):
        filters = []

        if 'id_paciente' in self._params:
            filters.append(self.citas.c.id_paciente == self._params['id_paciente'])

        filters.append(self.citas.c.id_doctor == self._params['id_doctor'])
        
        if self._params['fecha'] != 'all':
            filters.append(
                cast(self.citas.c.fecha_agendada, Date) == cast(self._params['fecha'], Date))

        return filters

    def list_appointments(self):
        """
        Methot that list all the appointments given a certain dates.
        """
        appointments = self.engine.execute(
                            select([
                                self.citas.c.id,
                                self.citas.c.id_paciente,
                                self.citas.c.fecha_agendada,
                                (cast(self.persons.c.nombre, String) + " " + \
                                 cast(self.persons.c.apellido_paterno, String) + " " + \
                                 cast(self.persons.c.apellido_materno, String)).label('nombre')]).\
                            select_from(self.citas.\
                                outerjoin(
                                    self.table,
                                    self.table.c.id ==
                                    self.citas.c.id_paciente).\
                                outerjoin(
                                    self.persons,
                                    self.persons.c.id ==
                                    self.table.c.id_persona)).\
                            where(
                                and_(*self.patient_citas_filters())).\
                            order_by(desc('fecha_agendada'))).fetchall()
        return format_appointments(appointments), 200

    def delete_appointment(self):
        """
        Method that deletes an appoitnment.
        """
        transaction = self._connection.begin()
        try:
            self._connection.execute(
                self.citas.delete().\
                where(self.citas.c.id == self._params['id']))
            transaction.commit()
            return {'status': 'Cita borrado correctamente'}, 200
        except Exception as e:
            logging.error("No se puedo borrar la cita")
            logging.exception(str(e))
            transaction.rollback()
            return {'error': "No se puedo borrar la cita"}, 500

    def update_appointment(self):
        """
        Method that updates the information of a patient.
        """
        transaction = self._connection.begin()
        try:
            self._connection.execute(
                self.citas.update().\
                where(self.citas.c.id == self._params['id']).\
                values(**self._params))
            transaction.commit()
            return {'status': 'Cita actualizada correctamente'}, 200
        except Exception as e:
            logging.error("No se puedo actualizar la cita")
            logging.exception(str(e))
            transaction.rollback()
            return {'error': "No se pudo actualizar la cita"}, 500

    def list_catalogue_estado_civil(self):
        catalogue_info = self.engine.execute(
            select([
                self.cat_estado_civil])).fetchall()
        return {info.id: info.tipo for info in catalogue_info}, 200

    def list_catalogue_ocupacion(self):
        catalogue_info = self.engine.execute(
            select([
                self.cat_ocupacion])).fetchall()
        return {info.id: info.ocupacion for info in catalogue_info}, 200

    def list_analysis(self):
        analysis = self.engine.execute(
            select([
                self.reportes.c.id,
                self.reportes.c.url_reporte]).\
            where(self.reportes.c.id_paciente == self._params['id'])
        ).fetchall()
        return format_analysis(analysis), 200

    def get_analysis(self):
        response = get_pdf_url(self._params['url'])
        return {'url': response}, 200