from eyechecker.factories.person_factory import PersonFactory

class Command:
    """
    Class that represents the Command Design Pattern.
    """
    def __init__(self, params, person_type):
        self._params = params
        self._person = PersonFactory(params).load(person_type)
        self._result = None
        self._status = None

    @property
    def result(self):
        return self._result

    @property
    def status(self):
        return self._status

    def execute(self, method_name):
        method = getattr(self._person, method_name)
        self._result, self._status = method()