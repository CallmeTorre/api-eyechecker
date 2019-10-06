from abc import ABCMeta, abstractmethod, abstractproperty

from sqlalchemy import Table

from eyechecker.utils.connection import engine, meta
from eyechecker.utils.formatter import format_person

class Person(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, params):
        self._engine = engine
        self._meta = meta
        self._params = params
        self._persons = Table(
            'personas',
            self.meta,
            autoload=True,
            autoload_with=self.engine)
        self._connection = self.engine.connect()

    @property
    def engine(self):
        return self._engine

    @property
    def meta(self):
        return self._meta

    @property
    def persons(self):
        return self._persons

    @abstractproperty
    def table(self):
        pass

    def _insert_person(self):
        transaction = self._connection.begin()
        person = format_person(self._params)
        try:
            id_person = self._connection.execute(
                self.persons.insert().values(**person)).inserted_primary_key[0]
            transaction.commit()
            return id_person
        except Exception as e:
            logging.error("No se puedo crear la persona")
            logging.exception(str(e))
            transaction.rollback()
            raise

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def update(self):
        pass