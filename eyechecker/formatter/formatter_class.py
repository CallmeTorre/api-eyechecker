class Formatter:
    """
    Class that format the response that will be send
    to the frontend.
    """

    def __init__(self):
        pass

    def newpatientformatter(self, id_patient):
        """
        Method that format the response when a new
        patient is created.
        """
        return {'id_paciente': id_patient}