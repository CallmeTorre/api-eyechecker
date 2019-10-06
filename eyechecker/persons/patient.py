import logging

from sqlalchemy import Table

from eyechecker.persons.person import Person
from eyechecker.utils.formatter import format_patient

class Patient(Person):

    def __init__(self, params):
        super().__init__(params)
        self._table = Table(
            'pacientes',
            self.meta,
            autoload=True,
            autoload_with=self.engine)

    @property
    def table(self):
        return self._table

    def create(self):
        transaction = self._connection.begin()
        self._params['id_persona'] = self._insert_person()
        patient = format_patient(self._params)
        try:
            raise Exception
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

    def delete(self):
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

    def update(self):
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