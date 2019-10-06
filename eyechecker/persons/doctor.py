from sqlalchemy import Table

from eyechecker.persons.person import Person
from eyechecker.utils.formatter import format_doctor

class Doctor(Person):

    def __init__(self, params):
        super().__init__(params)
        self._table = Table(
            'doctores',
            self.meta,
            autoload=True,
            autoload_with=self.engine)

    @property
    def table(self):
        return self._table

    def create(self):
        self._params['id_persona'] = self._insert_person()
        if self._params['id_persona'] != None:
            doctor = format_doctor(self._params)
            try:
                id = self.engine.execute(
                    self.table.insert().values(**doctor)).inserted_primary_key[0]
                return {'id_doctor': id,
                        'id_persona': self._params['id_persona']}, 200
            except Exception as e:
                logging.error("No se puedo crear el doctor")
                logging.exception(str(e))
                return {'error': "No se puedo crear el doctor"}, 500
        else:
            return {'error': "No se puedo crear el doctor"}, 500

    def delete(self):
        try:
            self.engine.execute(
                self.persons.delete().\
                where(self.persons.c.id == self._params['id']))
            return {'status': 'Doctor borrado correctamente'}, 200
        except Exception as e:
            logging.error("No se puedo borrar el doctor")
            logging.exception(str(e))
            return {'error': "No se puedo borrar el doctor"}, 500

    def update(self):
        try:
            self.engine.execute(
                self.table.update().\
                where(self.table.c.id == self._params['id']).\
                values(**self._params))
            return {'status': 'Doctor actualizado correctamente'}, 200
        except Exception as e:
            logging.error("No se puedo actualizar el doctor")
            logging.exception(str(e))
            return {'error': "No se puedo actualizar el doctor"}, 500