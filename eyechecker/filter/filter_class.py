from copy import deepcopy

from sqlalchemy import desc
from sqlalchemy.sql.expression import nullslast

from eyechecker.information.information_class import Information

class Filter:
    """
    Class that applies the filters given in a request
    """

    def __init__(self):
        self.information = Information()

    def _checkcondition(self, key, value):
        """
        Method that checks if the key is different to none
        so we can store the filter.
        """
        if value != 'all':
            return self.information.patientindexview_table.\
                c[key].ilike('%' + value + '%')

    def patientindexfilter(self, params):
        """
        Method that returns the filters for the patient's index.
        """
        filters = []
        params_copy = deepcopy(params)
        params_copy.pop('orderBy')

        for key, value in params_copy.items():
            condition = self._checkcondition(key, value)
            if condition is not None:
                filters.append(condition)

        return filters

    def _orderfield(self, criterion, orderings):
        """
        Method that allows us to know the ordering type of the query.
        Ex: DESC or ASC.
        """
        if criterion[-1] in ('+', '-'):
            direction = criterion[-1]
            fieldname = criterion[:-1]
        else:
            direction = None
            fieldname = criterion
        expression = orderings[fieldname]

        return expression if direction == '+' else nullslast(desc(expression))

    def orderargument(self, params):
        """
        Method that let us know the order criteria.
        """
        criteria = params['orderBy']

        # If the apram orderBy is not present,
        # a None value serves as a placeholder for
        # order_by
        if criteria == 'all':
            return []

        orderings = {
            'nombre': self.information.patientindexview_table.c.nombre,
            'apellido_paterno': self.information.patientindexview_table.c.apellido_paterno,
            'email': self.information.patientindexview_table.c.email}

        expression = self._orderfield(
                        criteria,
                        orderings)

        filtered = [expression]

        return filtered