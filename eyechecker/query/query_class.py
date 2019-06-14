from sqlalchemy.sql import select, and_

from eyechecker.information.information_class import Information
from eyechecker.filter.filter_class import Filter

class Query:
    """
    Class that contains all the queries used in the application.
    """

    def __init__(self):
        self.information = Information()
        self.filter = Filter()

    def newpatientquery(self, params):
        """
        Query used to insert a new patient information.
        """
        return self.information.patient_table.insert().values(**params)

    def _patientindexbasequery(self, params):
        """
        Base query used to get all the patients given a specific filter.
        """
        return select([self.information.patientindexview_table]).\
            where(and_(
                *self.filter.patientindexfilter(
                    params)))

    def patientindexquery(self, params):
        return self._patientindexbasequery(params).\
            order_by(*self.filter.orderargument(
                params))