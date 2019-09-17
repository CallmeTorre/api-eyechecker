import logging

from sqlalchemy import Table

from eyechecker.persons.person import Person

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
        try:
            id = self.engine.execute(
                self.table.insert().values(**self._params)).inserted_primary_key[0]
            return {'id_paciente': id}, 200
        except Exception as e:
            logging.error("No se puedo crear el paciente")
            logging.exception(str(e))
            return {'error': "No se puedo crear el paciente"}, 500

    def delete(self):
        try:
            self.engine.execute(
                self.table.delete().\
                where(self.table.c.curp == self._params['curp']))
            return {'status': 'Paciente borrado correctamente'}, 200
        except Exception as e:
            logging.error("No se puedo borrar el paciente")
            logging.exception(str(e))
            return {'error': "No se puedo borrar el paciente"}, 500

    def update(self):
        try:
            self.engine.execute(
                self.table.update().\
                where(self.table.c.curp == self._params['curp']).\
                values(**self._params))
            return {'status': 'Paciente actualizado correctamente'}, 200
        except Exception as e:
            logging.error("No se puedo actualizar el paciente")
            logging.exception(str(e))
            return {'error': "No se puedo actualizar el paciente"}, 500