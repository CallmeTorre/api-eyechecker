import logging
from inspect import getmembers, isclass, isabstract
from importlib import import_module

from eyechecker.factories.abs_factory import Factory
from eyechecker.persons.person import Person

class PersonFactory(Factory):

    def __init__(self, params):
        self._params = params

    def load(self, person_type):
        """
        Method that receives a person type and loads its class
        """
        try:
            module = import_module('.persons.' + person_type,
                                   'eyechecker')
        except ImportError:
            logging.error("Can't load %s class." % person_type)
            raise ImportError

        classes = getmembers(module,
                    lambda m: isclass(m) and not isabstract(m))

        for name, _class in classes:
            if issubclass(_class, Person):
                return _class(self._params)
