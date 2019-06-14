from eyechecker.utils.connection import engine
from eyechecker.query.query_class import Query
from eyechecker.formatter.formatter_class import Formatter

class Response:

    def __init__(self):
        self.query = Query()
        self.formatter = Formatter()

    def newpatientresponse(self, params):
        id_patient = engine.execute(
            self.query.newpatientquery(params)).inserted_primary_key[0]
        return self.formatter.newpatientformatter(id_patient), 200
