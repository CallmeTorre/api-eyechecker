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
        """
        Result from the specified method execution.
        """
        return self._result

    @property
    def status(self):
        """
        Result status from the specified method exuction
        """
        return self._status

    @classmethod
    def execute(self, method_name):
        """
        Method that execute a specified method from a class.
        """
        method = getattr(self._person, method_name)
        self._result, self._status = method()