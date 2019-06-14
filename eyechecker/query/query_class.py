from eyechecker.information.information_class import Information

class Query:
    """
    Class that contains all the queries used in the application.
    """

    def __init__(self):
        self.information = Information()

    def newpatientquery(self, params):
        """
        Query used to insert a new patient information.
        """
        return self.information.patient_table.insert().values(**params)