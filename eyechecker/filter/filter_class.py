from sqlalchemy import desc
from sqlalchemy.sql.expression import nullslast

from eyechecker.information.information_class import Information

class Filter:
    """
    Class that applies the filters given in a request
    """

    def __init__(self):
        self.information = Information()

    def patientindexfilter(self, params):
        """
        Method that returns the filters for the patient's index.
        """
        filters = []
        if params['nombre'] != 'all':
            filters.append(
                self.information.patientindexview_table.c.\
                    nombre.ilike('%' + params['nombre'] + '%'))

        if params['apellido_paterno'] != 'all':
            filters.append(
                self.information.patientindexview_table.c.\
                    nombre.ilike('%' + params['apellido_paterno'] + '%'))

        if params['email'] != 'all':
            filters.append(
                self.information.patientindexview_table.c.\
                    nombre.ilike('%' + params['email'] + '%'))

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