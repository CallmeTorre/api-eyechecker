from eyechecker.response import Response

class Command:
    """
    Class that represents the Command Design Pattern.
    """
    def __init__(self, params):
        self._params = params
        self._response = Response()
        self._result = None
        self._status = None

    @property
    def result(self):
        return self._result

    @property
    def status(self):
        return self._status

    def execute(self, method_name):
        method = getattr(self._response, method_name)
        self._result, self._status = method(self._params)