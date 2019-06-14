from sqlalchemy import Table

from eyechecker.utils.connection import engine, meta

class Information:

    def __init__(self):
        self._engine = engine
        self._meta = meta
        self._patient_table = Table(
            'pacientes',
            self.meta,
            autoload=True,
            autoload_with=self.engine)


    @property
    def engine(self):
        return self._engine

    @property
    def meta(self):
        return self._meta

    @property
    def patient_table(self):
        return self._patient_table
