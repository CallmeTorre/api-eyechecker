from abc import ABCMeta, abstractmethod, abstractproperty

from eyechecker.utils.connection import engine, meta

class Person(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, params):
        self._engine = engine
        self._meta = meta
        self._params = params

    @property
    def engine(self):
        return self._engine

    @property
    def meta(self):
        return self._meta

    @abstractproperty
    def table(self):
        pass

    @abstractmethod
    def create(self):
        pass