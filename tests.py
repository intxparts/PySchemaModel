import psm
import unittest

class is_built_in_name_tests(unittest.TestCase):
    def test_success(self):
        self.assertTrue(psm._is_builtin_name('__name__'))

    def test_failure_cases(self):
        for t in [True, [], {}, 1, -2.1, None, '__data', '__data_', 'data__', '_data__']:
            self.assertFalse(psm._is_builtin_name(t))

class BoolField_tests(unittest.TestCase):
    def test_validation_required_enabled(self):
        class Model(psm.SchemaModel):
            field = psm.BoolField(required=True)
        
        m1 = Model()
        missing_result, missing_errors = m1.validate()
        self.assertFalse(missing_result)
        self.assertEqual(1, len(missing_errors))

        m2 = Model(field=True)
        result, errors = m2.validate()
        self.assertTrue(result)
        self.assertEqual(0, len(errors))

    def test_validation_required_disabled(self):
        class Model(psm.SchemaModel):
            field = psm.BoolField(required=False)

        m1 = Model()
        missing_result, missing_errors = m1.validate()
        self.assertTrue(missing_result)
        self.assertEqual(0, len(missing_errors))

    def test_validation_nullable_bool(self):
        class Model(psm.SchemaModel):
            field = psm.BoolField(nullable=True)
        
        m1 = Model(field=None)
        null_result, null_errors = m1.validate()
        self.assertTrue(null_result)
        self.assertEqual(0, len(null_errors))

        m2 = Model(field=False)
        non_null_result, non_null_errors = m2.validate()
        self.assertTrue(non_null_result)
        self.assertEqual(0, len(non_null_errors))

    def test_validation_nonnullable_bool(self):
        class Model(psm.SchemaModel):
            field = psm.BoolField(nullable=False)
        
        m1 = Model(field=None)
        null_result, null_errors = m1.validate()
        self.assertFalse(null_result)
        self.assertEqual(1, len(null_errors))

        m2 = Model(field=True)
        nonnull_result, nonnull_errors = m2.validate()
        self.assertTrue(nonnull_result)
        self.assertEqual(0, len(nonnull_errors))

    def test_serialize_nullable_bool(self):
        class Model(psm.SchemaModel):
            field = psm.BoolField(nullable=True)
        
        m1 = Model(field=None)
        m1_str = psm.serialize(m1)
        self.assertEqual('{"field": null}', m1_str)

        m2 = Model(field=False)
        m2_str = psm.serialize(m2)
        self.assertEqual('{"field": false}', m2_str)

        m3 = Model(field=True)
        m3_str = psm.serialize(m3)
        self.assertEqual('{"field": true}', m3_str)

    def test_deserialize_nullable_bool(self):
        class Model(psm.SchemaModel):
            field = psm.BoolField(nullable=True)

        null_model = psm.deserialize(Model, '{"field": null}')
        self.assertEqual(None, null_model.field)

        false_model = psm.deserialize(Model, '{"field": false}')
        self.assertEqual(False, false_model.field)

        true_model = psm.deserialize(Model, '{"field": true}')
        self.assertEqual(True, true_model.field)

        # additional fields
        with self.assertRaises(psm.ValidationError):
            psm.deserialize(Model, '{"field": null, "greeting": "hello"}')

        # missing fields
        with self.assertRaises(psm.ValidationError):
            psm.deserialize(Model, '{"another_field": null}')

    def test_serialize_bool(self):
        class Model(psm.SchemaModel):
            field = psm.BoolField(nullable=False)
        
        m1 = Model(field=None)
        with self.assertRaises(psm.ValidationError):
            psm.serialize(m1)

        m2 = Model(field=False)
        m2_str = psm.serialize(m2)
        self.assertEqual('{"field": false}', m2_str)

        m3 = Model(field=True)
        m3_str = psm.serialize(m3)
        self.assertEqual('{"field": true}', m3_str)

    def test_deserialize_bool(self):
        class Model(psm.SchemaModel):
            field = psm.BoolField(nullable=False)

        with self.assertRaises(psm.ValidationError):
            psm.deserialize(Model, '{"field": null}')

        false_model = psm.deserialize(Model, '{"field": false}')
        self.assertEqual(False, false_model.field)

        true_model = psm.deserialize(Model, '{"field": true}')
        self.assertEqual(True, true_model.field)

class StringField_tests(unittest.TestCase):
    def test_validation_required_enabled(self):
        class Model(psm.SchemaModel):
            field = psm.StringField(required=True)

        m1 = Model()
        missing_result, missing_errors = m1.validate()
        self.assertFalse(missing_result)
        self.assertEqual(1, len(missing_errors))

        m2 = Model(field='str')
        result, errors = m2.validate()
        self.assertTrue(result)
        self.assertEqual(0, len(errors))

    def test_validation_required_disabled(self):
        class Model(psm.SchemaModel):
            field = psm.StringField(required=False)

        m1 = Model()
        missing_result, missing_errors = m1.validate()
        self.assertTrue(missing_result)
        self.assertEqual(0, len(missing_errors))

    def test_validation_nullable_string(self):
        class Model(psm.SchemaModel):
            field = psm.StringField(nullable=True)
        
        m1 = Model(field=None)
        null_result, null_errors = m1.validate()
        self.assertTrue(null_result)
        self.assertEqual(0, len(null_errors))

        m2 = Model(field='str')
        non_null_result, non_null_errors = m2.validate()
        self.assertTrue(non_null_result)
        self.assertEqual(0, len(non_null_errors))

    def test_validation_nonnullable_string(self):
        class Model(psm.SchemaModel):
            field = psm.StringField(nullable=False)
        
        m1 = Model(field=None)
        null_result, null_errors = m1.validate()
        self.assertFalse(null_result)
        self.assertEqual(1, len(null_errors))

        m2 = Model(field='str')
        nonnull_result, nonnull_errors = m2.validate()
        self.assertTrue(nonnull_result)
        self.assertEqual(0, len(nonnull_errors))


    def test_validation_allowed(self):
        class Model(psm.SchemaModel):
            field = psm.StringField(allowed=['square', 'circle'])

        m1 = Model(field='str')
        invalid_str_result, invalid_str_errors = m1.validate()
        self.assertFalse(invalid_str_result)
        self.assertEqual(1, len(invalid_str_errors))

        m2 = Model(field='square')
        valid_str_result, valid_str_errors = m2.validate()
        self.assertTrue(valid_str_result)
        self.assertEqual(0, len(valid_str_errors))

        m3 = Model(field='circle')
        valid_str_result2, valid_str_errors2 = m3.validate()
        self.assertTrue(valid_str_result2)
        self.assertEqual(0, len(valid_str_errors2))

    def test_validation_forbidden(self):
        class Model(psm.SchemaModel):
            field = psm.StringField(forbidden=['square', 'circle'])
        
        m1 = Model(field='str')
        valid_str_result, valid_str_errors = m1.validate()
        self.assertTrue(valid_str_result)
        self.assertEqual(0, len(valid_str_errors))

        m2 = Model(field='square')
        invalid_str_result1, invalid_str_errors1 = m2.validate()
        self.assertFalse(invalid_str_result1)
        self.assertEqual(1, len(invalid_str_errors1))

        m3 = Model(field='circle')
        invalid_str_result2, invalid_str_errors2 = m3.validate()
        self.assertFalse(invalid_str_result2)
        self.assertEqual(1, len(invalid_str_errors2))

    def test_serialize_nullable_string(self):
        class Model(psm.SchemaModel):
            field = psm.StringField(nullable=True)
        
        m1 = Model(field=None)
        m1_str = psm.serialize(m1)
        self.assertEqual('{"field": null}', m1_str)

        m2 = Model(field='str')
        m2_str = psm.serialize(m2)
        self.assertEqual('{"field": "str"}', m2_str)

        m3 = Model(field='')
        m3_str = psm.serialize(m3)
        self.assertEqual('{"field": ""}', m3_str)

    def test_serialize_nonnullable_string(self):
        class Model(psm.SchemaModel):
            field = psm.StringField(nullable=False)
        
        m1 = Model(field=None)
        with self.assertRaises(psm.ValidationError):
            psm.serialize(m1)

        m2 = Model(field='str')
        m2_str = psm.serialize(m2)
        self.assertEqual('{"field": "str"}', m2_str)

        m3 = Model(field='')
        m3_str = psm.serialize(m3)
        self.assertEqual('{"field": ""}', m3_str)

    def test_deserialize_nullable_string(self):
        class Model(psm.SchemaModel):
            field = psm.StringField(nullable=True)

        null_model = psm.deserialize(Model, '{"field": null}')
        self.assertEqual(None, null_model.field)

        nonempty_model = psm.deserialize(Model, '{"field": "str"}')
        self.assertEqual('str', nonempty_model.field)

        empty_model = psm.deserialize(Model, '{"field": ""}')
        self.assertEqual('', empty_model.field)

        # additional fields
        with self.assertRaises(psm.ValidationError):
            psm.deserialize(Model, '{"field": null, "greeting": "hello"}')

        # missing fields
        with self.assertRaises(psm.ValidationError):
            psm.deserialize(Model, '{"another_field": null}')

    def test_deserialize_nonnullable_string(self):
        class Model(psm.SchemaModel):
            field = psm.StringField(nullable=False)

        with self.assertRaises(psm.ValidationError):
            psm.deserialize(Model, '{"field": null}')

        nonempty_model = psm.deserialize(Model, '{"field": "str"}')
        self.assertEqual('str', nonempty_model.field)

        empty_model = psm.deserialize(Model, '{"field": ""}')
        self.assertEqual('', empty_model.field)

class IntegerField_tests(unittest.TestCase):
    def test_validation_required_enabled(self):
        pass

    def test_validation_required_disabled(self):
        pass

    def test_validation_nullable(self):
        pass

    def test_validation_nonnullable(self):
        pass

    def test_validation_allowed(self):
        pass

    def test_validation_forbidden(self):
        pass

    def test_validation_min(self):
        pass

    def test_validation_max(self):
        pass

    def test_serialize_nullable(self):
        pass

    def test_serialize(self):
        pass

    def test_deserialize_nullable(self):
        pass

    def test_deserialize(self):
        pass

class FloatField_tests(unittest.TestCase):
    def test_validation_required_enabled(self):
        pass

    def test_validation_required_disabled(self):
        pass

    def test_validation_nullable(self):
        pass

    def test_validation_nonnullable(self):
        pass

    def test_validation_allowed(self):
        pass

    def test_validation_forbidden(self):
        pass

    def test_validation_min(self):
        pass

    def test_validation_max(self):
        pass

    def test_serialize_nullable(self):
        pass

    def test_serialize(self):
        pass

    def test_deserialize_nullable(self):
        pass

    def test_deserialize(self):
        pass

class ListField_tests(unittest.TestCase):
    pass

class DictField_tests(unittest.TestCase):
    pass

class ObjectField_tests(unittest.TestCase):
    pass

class Complex_tests(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()