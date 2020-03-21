from unittest import TestCase, main

from schema import SchemaMissingKeyError

from tests.test_variables import (patientparams,
                                  doctorparams,
                                  patientlistparams,
                                  resetpasswordparams,
                                  analysisparams,
                                  appointmentparams,
                                  loginparams)
from eyechecker.utils.schemas import (patientschema, 
                                      doctorschema, 
                                      patientlistschema,
                                      resetpasswordschema,
                                      analysisschema,
                                      appointmentschema,
                                      loginschema)
class TestPatientSchemas(TestCase):

    def setUp(self):
        self.schema = patientschema
        self.params = patientparams.copy()

    def test_valid(self):
        self.schema.validate(self.params)


class TestDoctorSchemas(TestCase):

    def setUp(self):
        self.schema = doctorschema
        self.params = doctorparams.copy()

    def test_valid(self):
        self.schema.validate(self.params)


class TestPatientListSchemas(TestCase):

    def setUp(self):
        self.schema = patientlistschema
        self.params = patientlistparams.copy()

    def test_valid(self):
        self.schema.validate(self.params)

    def test_missing_nombre(self):
        self.params.pop('nombre')
        with self.assertRaises(SchemaMissingKeyError) as context:
            self.schema.validate(self.params)
        self.assertEqual(
            str(context.exception),
            "Missing key: 'nombre'")

    def test_missing_curp(self):
        self.params.pop('curp')
        with self.assertRaises(SchemaMissingKeyError) as context:
            self.schema.validate(self.params)
        self.assertEqual(
            str(context.exception),
            "Missing key: 'curp'")


class TestResetPasswordSchemas(TestCase):

    def setUp(self):
        self.schema = resetpasswordschema
        self.params = resetpasswordparams.copy()

    def test_valid(self):
        self.schema.validate(self.params)


class TestAnalysisSchemas(TestCase):

    def setUp(self):
        self.schema = analysisschema
        self.params = analysisparams.copy()

    def test_valid(self):
        self.schema.validate(self.params)

    def test_missing_id(self):
        self.params.pop('id')
        with self.assertRaises(SchemaMissingKeyError) as context:
            self.schema.validate(self.params)
        self.assertEqual(
            str(context.exception),
            "Missing key: 'id'")


class TestAppointmentSchemas(TestCase):

    def setUp(self):
        self.schema = appointmentschema
        self.params = appointmentparams.copy()

    def test_valid(self):
        self.schema.validate(self.params)


class TestLoginSchemas(TestCase):

    def setUp(self):
        self.schema = loginschema
        self.params = loginparams.copy()

    def test_valid(self):
        self.schema.validate(self.params)

    def test_missing_nombre(self):
        self.params.pop('usuario')
        with self.assertRaises(SchemaMissingKeyError) as context:
            self.schema.validate(self.params)
        self.assertEqual(
            str(context.exception),
            "Missing key: 'usuario'")

    def test_missing_curp(self):
        self.params.pop('password')
        with self.assertRaises(SchemaMissingKeyError) as context:
            self.schema.validate(self.params)
        self.assertEqual(
            str(context.exception),
            "Missing key: 'password'")


if __name__ == '__main__':
    main()