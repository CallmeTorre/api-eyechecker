import logging

from sqlalchemy import Table

from eyechecker.persons.person import Person
from eyechecker.utils.formatter import (format_doctor, format_account)

class Doctor(Person):
    """
    Class that defines main doctor's operations.
    """

    def __init__(self, params):
        """
        Doctor's constructor method.
        """
        super().__init__(params)
        self._table = Table(
            'doctores',
            self.meta,
            autoload=True,
            autoload_with=self.engine)
        self._account = Table(
            'cuentas',
            self.meta,
            autoload=True,
            autoload_with=self.engine)

    @property
    def table(self):
        """
        Doctor's table
        """
        return self._table

    @property
    def account(self):
        """
        Account's table
        """
        return self._account

    #@classmethod
    def _create_account(self):
        """
        Private method that creates a new doctor's account.
        """
        transaction = self._connection.begin()
        account = format_account(self._params)
        try:
            self._connection.execute(
                self.account.insert().values(**account)).inserted_primary_key[0]
            transaction.commit()
        except Exception as e:
            logging.error("No se puedo crear la cuenta")
            logging.exception(str(e))
            transaction.rollback()

    #@classmethod
    def create(self):
        """
        Method that creates a new doctor in the database.
        """
        transaction = self._connection.begin()
        self._params['id_persona'] = self._insert_person()
        doctor = format_doctor(self._params)
        try:
            self._params['id_doctor'] = self._connection.execute(
                self.table.insert().values(**doctor)).inserted_primary_key[0]
            self._create_account()
            transaction.commit()
            return {'id_doctor': self._params['id_doctor'],
                    'id_persona': self._params['id_persona']}, 200
        except Exception as e:
            logging.error("No se puedo crear el doctor")
            logging.exception(str(e))
            transaction.rollback()
            return {'error': "No se puedo crear el doctor"}, 500

    #@classmethod
    def delete(self):
        """
        Method that deletes a doctor.
        """
        transaction = self._connection.begin()
        try:
            self._connection.execute(
                self.persons.delete().\
                where(self.persons.c.id == self._params['id']))
            transaction.commit()
            return {'status': 'Doctor borrado correctamente'}, 200
        except Exception as e:
            logging.error("No se puedo borrar el doctor")
            logging.exception(str(e))
            transaction.rollback()
            return {'error': "No se puedo borrar el doctor"}, 500

    #@classmethod
    def update(self):
        """
        Method that updates the information of a doctor.
        """
        try:
            self._connection.execute(
                self.table.update().\
                where(self.table.c.id == self._params['id']).\
                values(**self._params))
            transaction.commit()
            return {'status': 'Doctor actualizado correctamente'}, 200
        except Exception as e:
            logging.error("No se puedo actualizar el doctor")
            logging.exception(str(e))
            transaction.rollback()
            return {'error': "No se puedo actualizar el doctor"}, 500

    def get(self):
        return ":D", 200