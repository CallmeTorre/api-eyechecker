import logging

from sqlalchemy import Table
from sqlalchemy.sql import select

from eyechecker.persons.person import Person
from eyechecker.utils.formatter import (format_doctor, format_account)
from eyechecker.utils.notifications import send_recover_email

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
        transaction = self._connection.begin()
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
        """
        Method that retrieves the information of a patient.
        """
        doctor_info = self.engine.execute(
                            select([
                                self.persons,
                                self.table]).\
                            select_from(self.table.\
                                outerjoin(
                                    self.persons,
                                    self.persons.c.id ==
                                    self.table.c.id_persona)).\
                            where(self.persons.c.id == self._params['id'])).fetchone()
        return {
            'nombre': doctor_info.nombre + " " + doctor_info.apellido_paterno + " " + doctor_info.apellido_materno,
            'email': doctor_info.email,
            'telefono_celular': doctor_info.telefono_celular,
            'genero': doctor_info.genero,
            'organizacion': doctor_info.organizacion,
            'cedula': doctor_info.cedula,
            'horario': doctor_info.horario
        }, 200

    def reset_password(self):
        """
        Method that reset the password of the account.
        """
        transaction = self._connection.begin()
        user = self._connection.execute(
                select([self.account.c.id]).\
                where(self.account.c.usuario == self._params['usuario'])).fetchone()
        if user != None:
            try:
                self._connection.execute(
                    self.account.update().\
                    where(self.account.c.usuario == self._params['usuario']).\
                    values(password=self._params['password']))
                transaction.commit()
                return {'status': 'Password actualizado correctamente'}, 200
            except Exception as e:
                logging.error("No se pudo reestablecer el password")
                logging.exception(str(e))
                transaction.rollback()
                return {'error': "No se pudo reestablecer el password"}, 500
        else:
            return {'error': "Usario no existente"}, 404

    def recover_password(self):
        """
        Method that recovers the password for an account.
        """
        transaction = self._connection.begin()
        user = self._connection.execute(
                select([
                    self.account.c.id,
                    self.persons.c.email]).\
                select_from(self.account.\
                    outerjoin(
                        self.table,
                        self.table.c.id ==
                        self.account.c.id_doctor).\
                    outerjoin(
                        self.persons,
                        self.persons.c.id ==
                        self.table.c.id_persona
                    )).\
                where(self.account.c.usuario == self._params['usuario'])).fetchone()
        if user != None:
            return send_recover_email(user.email)
        else:
            return {'error': "Usario no existente"}, 404
    
    def validate_login(self):
        """
        Method that validate the users information.
        """
        account_info = self.engine.execute(
            select([
                    self.account.c.id,
                    self.account.c.usuario,
                    self.account.c.password]).\
                select_from(self.account.\
                    outerjoin(
                        self.table,
                        self.table.c.id ==
                        self.account.c.id_doctor).\
                    outerjoin(
                        self.persons,
                        self.persons.c.id ==
                        self.table.c.id_persona
                    )).\
                where(self.account.c.usuario == self._params['usuario'])).fetchone()
        if account_info == None:
            return {'access': False}
        elif account_info.password == self._params['password']:
            return {'access': False}
        else:
            return {'access': True}