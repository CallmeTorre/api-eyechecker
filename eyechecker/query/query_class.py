from eyechecker.information.information_class import Information

class Query:

    def __init__(self):
        self.information = Information()

    def newpatientquery(self, params):
        return self.information.patient_table.insert().values(**params)