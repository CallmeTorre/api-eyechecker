from sqlalchemy import Table

from eyechecker.persons.person import Person

class Doctor(Person):

    def __init__(self, params):
        super().__init__(params)