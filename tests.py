import psm
import unittest

class is_built_in_name_tests(unittest.TestCase):
    def test_success(self):
        self.assertTrue(psm.is_builtin_name('__name__'))

    def test_failure_cases(self):
        for t in [True, [], {}, 1, -2.1, None, '__data', '__data_', 'data__', '_data__']:
            self.assertFalse(psm.is_builtin_name(t))

class serialize_tests(unittest.TestCase):
    def test_type_error(self):
        with self.assertRaisesRegex(TypeError, "Object must be an instance of a SchemaModel"):
            psm.serialize(10)

    def test_validation_error(self):
        class A(psm.SchemaModel):
            name = { 'required'  : True, 'type': 'string' }

        a = A()
        with self.assertRaises(psm.CerberusValidationError):
            psm.serialize(a)

    def test_success(self):
        class A(psm.SchemaModel):
            name = { 'required'  : True, 'type': 'string' }
        a = A(name='Name')
        s = psm.serialize(a)
        self.assertEqual(s, '{"name": "Name"}')

class deserialize_tests(unittest.TestCase):
    def test_type_error(self):
        class A:
            name = { 'required'  : True, 'type': 'string' }
        with self.assertRaisesRegex(TypeError, "Class must be a subclass of SchemaModel"):
            psm.deserialize(A, '{"name": "Name"}')
    
    def test_validation_error(self):
        class A(psm.SchemaModel):
            name = { 'required'  : True, 'type': 'string' }
            age = { 'required' : True, 'type' : 'integer' }

        with self.assertRaises(psm.CerberusValidationError):
            psm.deserialize(A, '{"age": 56}')

    def test_success(self):
        class A(psm.SchemaModel):
            name = { 'required'  : True, 'type': 'string' }
            age = { 'required' : True, 'type' : 'integer' }

        d = psm.deserialize(A, '{"name": "Name", "age": 56}')
        self.assertIsInstance(d, A)
        self.assertIsInstance(d, psm.SchemaModel)
        self.assertDictEqual({"name": "Name", "age": 56}, vars(d))

class SchemaModel_validate_tests(unittest.TestCase):
    pass

class SchemaModel_init_tests(unittest.TestCase):
    pass

class SchemaModel_setattr_tests(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()