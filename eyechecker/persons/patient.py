import logging

from sqlalchemy import Table, cast
from sqlalchemy.sql import select, and_
from sqlalchemy.types import String

from eyechecker.persons.person import Person
from eyechecker.utils.formatter import format_patient

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
                    'id_persona': self._params['id_persona']}, 200
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
                                    *self.patient_list_filters()))).fetchall()
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
        return {'patient_list': result}, 200