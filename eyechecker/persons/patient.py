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
        self._params['id_persona'] = self._insert_person()
        if self._params['id_persona'] != None:
            patient = format_patient(self._params)
            try:
                id = self.engine.execute(
                    self.table.insert().values(**patient)).inserted_primary_key[0]
                return {'id_paciente': id,
                        'id_persona': self._params['id_persona']}, 200
            except Exception as e:
                logging.error("No se puedo crear el paciente")
                logging.exception(str(e))
                return {'error': "No se puedo crear el paciente"}, 500
        else:
            return {'error': "No se puedo crear el paciente"}, 500

    def delete(self):
        try:
            self.engine.execute(
                self.persons.delete().\
                where(self.persons.c.id == self._params['id']))
            return {'status': 'Paciente borrado correctamente'}, 200
        except Exception as e:
            logging.error("No se puedo borrar el paciente")
            logging.exception(str(e))
            return {'error': "No se puedo borrar el paciente"}, 500

    def update(self):
        try:
            self.engine.execute(
                self.table.update().\
                where(self.table.c.id == self._params['id']).\
                values(**self._params))
            return {'status': 'Paciente actualizado correctamente'}, 200
        except Exception as e:
            logging.error("No se puedo actualizar el paciente")
            logging.exception(str(e))
            return {'error': "No se puedo actualizar el paciente"}, 500