from abc import (ABCMeta,
                 abstractmethod,
                 abstractproperty)

from sqlalchemy import Table

from eyechecker.utils.connection import engine, meta
from eyechecker.utils.formatter import format_person

class Person(metaclass=ABCMeta):
    """
    Abstract class that defines a person operations
    and common attributes.
    """

    @abstractmethod
    def __init__(self, params):
        """
        Person's constructor method.
        """
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
        """
        Database engine.
        """
        return self._engine

    @property
    def meta(self):
        """
        Database metadata.
        """
        return self._meta

    @property
    def persons(self):
        """
        Person's table.
        """
        return self._persons

    @abstractproperty
    def table(self):
        """
        Abstract property to define a patient or doctor table.
        """
        pass

    @classmethod
    def _insert_person(self):
        """
        Private method that creates a new person.
        """
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
        """
        Abstract method that defines a patient or doctor creation method.
        """
        pass

    @abstractmethod
    def delete(self):
        """
        Abstract method that defines a patient or doctor delete method.
        """
        pass

    @abstractmethod
    def update(self):
        """
        Abstract method that defines a patient or doctor update method.
        """
        pass