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
            logging.error("Can't create patient")
            logging.exception(str(e))
            return {'error': "Can't create the patient"}, 500
