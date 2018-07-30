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
        class Model(psm.SchemaModel):
            field = psm.IntegerField(required=True)

        m1 = Model()
        missing_result, missing_errors = m1.validate()
        self.assertFalse(missing_result)
        self.assertEqual(1, len(missing_errors))

        m2 = Model(field=12)
        result, errors = m2.validate()
        self.assertTrue(result)
        self.assertEqual(0, len(errors))


    def test_validation_required_disabled(self):
        class Model(psm.SchemaModel):
            field = psm.IntegerField(required=False)

        m1 = Model()
        missing_result, missing_errors = m1.validate()
        self.assertTrue(missing_result)
        self.assertEqual(0, len(missing_errors))

        m2 = Model(field=-10)
        result, errors = m2.validate()
        self.assertTrue(result)
        self.assertEqual(0, len(errors))

    def test_validation_nullable(self):
        class Model(psm.SchemaModel):
            field = psm.IntegerField(nullable=True)

        m1 = Model(field=None)
        null_result, null_errors = m1.validate()
        self.assertTrue(null_result)
        self.assertEqual(0, len(null_errors))

        m2 = Model(field=129)
        result, errors = m2.validate()
        self.assertTrue(result)
        self.assertEqual(0, len(errors))

    def test_validation_nonnullable(self):
        class Model(psm.SchemaModel):
            field = psm.IntegerField(nullable=False)

        m1 = Model(field=None)
        null_result, null_errors = m1.validate()
        self.assertFalse(null_result)
        self.assertEqual(1, len(null_errors))

        m2 = Model(field=11)
        result, errors = m2.validate()
        self.assertTrue(result)
        self.assertEqual(0, len(errors))

    def test_validation_allowed(self):
        class Model(psm.SchemaModel):
            field = psm.IntegerField(allowed=[1, 2, 3, 5, 7, 11, 13])

        m1 = Model(field=8)
        na_result, na_errors = m1.validate()
        self.assertFalse(na_result)
        self.assertEqual(1, len(na_errors))

        m2 = Model(field=11)
        result, errors = m2.validate()
        self.assertTrue(result)
        self.assertEqual(0, len(errors))

    def test_validation_forbidden(self):
        class Model(psm.SchemaModel):
            field = psm.IntegerField(forbidden=[1, 2, 3, 5, 7, 11, 13])

        m1 = Model(field=8)
        result, errors = m1.validate()
        self.assertTrue(result)
        self.assertEqual(0, len(errors))

        m2 = Model(field=11)
        na_result, na_errors = m2.validate()
        self.assertFalse(na_result)
        self.assertEqual(1, len(na_errors))

    def test_validation_min(self):
        class Model(psm.SchemaModel):
            field = psm.IntegerField(_min=-1)

        m1 = Model(field = 0)
        result, errors = m1.validate()
        self.assertTrue(result)
        self.assertEqual(0, len(errors))

        m2 = Model(field = -1)
        match_result, match_errors = m2.validate()
        self.assertTrue(match_result)
        self.assertEqual(0, len(match_errors))

        m3 = Model(field = -2)
        below_result, below_errors = m3.validate()
        self.assertFalse(below_result)
        self.assertEqual(1, len(below_errors))

    def test_validation_max(self):
        class Model(psm.SchemaModel):
            field = psm.IntegerField(_max=10)

        m1 = Model(field = 9)
        result, errors = m1.validate()
        self.assertTrue(result)
        self.assertEqual(0, len(errors))

        m2 = Model(field = 10)
        match_result, match_errors = m2.validate()
        self.assertTrue(match_result)
        self.assertEqual(0, len(match_errors))

        m3 = Model(field = 11)
        above_result, above_errors = m3.validate()
        self.assertFalse(above_result)
        self.assertEqual(1, len(above_errors))

    def test_serialize_nullable(self):
        class Model(psm.SchemaModel):
            field = psm.IntegerField(nullable=True)

        m1 = Model()
        m1_str = psm.serialize(m1)
        self.assertEqual('{}', m1_str)

        m2 = Model(field=None)
        m2_str = psm.serialize(m2)
        self.assertEqual('{"field": null}', m2_str)

        m3 = Model(field=12)
        m3_str = psm.serialize(m3)
        self.assertEqual('{"field": 12}', m3_str)

    def test_serialize_nonnullable(self):
        class Model(psm.SchemaModel):
            field = psm.IntegerField(nullable=False)

        m1 = Model(field=None)
        with self.assertRaises(psm.ValidationError):
            psm.serialize(m1)

        m2 = Model(field=12)
        m2_str = psm.serialize(m2)
        self.assertEqual('{"field": 12}', m2_str)

    def test_deserialize_nullable(self):
        class Model(psm.SchemaModel):
            field = psm.IntegerField(nullable=True)

        m1 = psm.deserialize(Model, '{"field": null}')
        self.assertEqual(None, m1.field)

        m2 = psm.deserialize(Model, '{"field": 12}')
        self.assertEqual(12, m2.field)

        with self.assertRaises(psm.ValidationError):
            psm.deserialize(Model, '{"field": "str"}')

        with self.assertRaises(psm.ValidationError):
            psm.deserialize(Model, '{"field": -1, "greeting": "hello"}')

        with self.assertRaises(psm.ValidationError):
            psm.deserialize(Model, '{"greeting": "hello"}')

    def test_deserialize_nonnullable(self):
        class Model(psm.SchemaModel):
            field = psm.IntegerField(nullable=False)

        with self.assertRaises(psm.ValidationError):
            psm.deserialize(Model, '{"field": null}')

        m1 = psm.deserialize(Model, '{"field": 12}')
        self.assertEqual(12, m1.field)


class FloatField_tests(unittest.TestCase):
    def test_validation_required_enabled(self):
        class Model(psm.SchemaModel):
            field = psm.FloatField(required=True)

        m1 = Model()
        missing_result, missing_errors = m1.validate()
        self.assertFalse(missing_result)
        self.assertEqual(1, len(missing_errors))

        m2 = Model(field=12.34)
        result, errors = m2.validate()
        self.assertTrue(result)
        self.assertEqual(0, len(errors))


    def test_validation_required_disabled(self):
        class Model(psm.SchemaModel):
            field = psm.FloatField(required=False)

        m1 = Model()
        missing_result, missing_errors = m1.validate()
        self.assertTrue(missing_result)
        self.assertEqual(0, len(missing_errors))

        m2 = Model(field=-10.1)
        result, errors = m2.validate()
        self.assertTrue(result)
        self.assertEqual(0, len(errors))

    def test_validation_nullable(self):
        class Model(psm.SchemaModel):
            field = psm.FloatField(nullable=True)

        m1 = Model(field=None)
        null_result, null_errors = m1.validate()
        self.assertTrue(null_result)
        self.assertEqual(0, len(null_errors))

        m2 = Model(field=129.987)
        result, errors = m2.validate()
        self.assertTrue(result)
        self.assertEqual(0, len(errors))

    def test_validation_nonnullable(self):
        class Model(psm.SchemaModel):
            field = psm.FloatField(nullable=False)

        m1 = Model(field=None)
        null_result, null_errors = m1.validate()
        self.assertFalse(null_result)
        self.assertEqual(1, len(null_errors))

        m2 = Model(field=11.1)
        result, errors = m2.validate()
        self.assertTrue(result)
        self.assertEqual(0, len(errors))

    def test_validation_allowed(self):
        class Model(psm.SchemaModel):
            field = psm.FloatField(allowed=[1.1, 2.2, 3.3, 5.5])

        m1 = Model(field=-1.2)
        na_result, na_errors = m1.validate()
        self.assertFalse(na_result)
        self.assertEqual(1, len(na_errors))

        m2 = Model(field=3.3)
        result, errors = m2.validate()
        self.assertTrue(result)
        self.assertEqual(0, len(errors))

    def test_validation_forbidden(self):
        class Model(psm.SchemaModel):
            field = psm.FloatField(forbidden=[1.1, 2.2, 3.3, 5.5])

        m1 = Model(field=8.5)
        result, errors = m1.validate()
        self.assertTrue(result)
        self.assertEqual(0, len(errors))

        m2 = Model(field=2.2)
        na_result, na_errors = m2.validate()
        self.assertFalse(na_result)
        self.assertEqual(1, len(na_errors))

    def test_validation_min(self):
        class Model(psm.SchemaModel):
            field = psm.FloatField(_min=-1.34)

        m1 = Model(field = -1.33)
        result, errors = m1.validate()
        self.assertTrue(result)
        self.assertEqual(0, len(errors))

        m2 = Model(field = -1.34)
        match_result, match_errors = m2.validate()
        self.assertTrue(match_result)
        self.assertEqual(0, len(match_errors))

        m3 = Model(field = -1.35)
        below_result, below_errors = m3.validate()
        self.assertFalse(below_result)
        self.assertEqual(1, len(below_errors))

    def test_validation_max(self):
        class Model(psm.SchemaModel):
            field = psm.FloatField(_max=10.12)

        m1 = Model(field = 10.1)
        result, errors = m1.validate()
        self.assertTrue(result)
        self.assertEqual(0, len(errors))

        m2 = Model(field = 10.12)
        match_result, match_errors = m2.validate()
        self.assertTrue(match_result)
        self.assertEqual(0, len(match_errors))

        m3 = Model(field = 10.2)
        above_result, above_errors = m3.validate()
        self.assertFalse(above_result)
        self.assertEqual(1, len(above_errors))

    def test_serialize_nullable(self):
        class Model(psm.SchemaModel):
            field = psm.FloatField(nullable=True)

        m1 = Model()
        m1_str = psm.serialize(m1)
        self.assertEqual('{}', m1_str)

        m2 = Model(field=None)
        m2_str = psm.serialize(m2)
        self.assertEqual('{"field": null}', m2_str)

        m3 = Model(field=12.12)
        m3_str = psm.serialize(m3)
        self.assertEqual('{"field": 12.12}', m3_str)

    def test_serialize_nonnullable(self):
        class Model(psm.SchemaModel):
            field = psm.FloatField(nullable=False)

        m1 = Model(field=None)
        with self.assertRaises(psm.ValidationError):
            psm.serialize(m1)

        m2 = Model(field=12.12)
        m2_str = psm.serialize(m2)
        self.assertEqual('{"field": 12.12}', m2_str)

    def test_deserialize_nullable(self):
        class Model(psm.SchemaModel):
            field = psm.FloatField(nullable=True)

        m1 = psm.deserialize(Model, '{"field": null}')
        self.assertEqual(None, m1.field)

        m2 = psm.deserialize(Model, '{"field": 12.34}')
        self.assertEqual(12.34, m2.field)

        with self.assertRaises(psm.ValidationError):
            psm.deserialize(Model, '{"field": "str"}')

        with self.assertRaises(psm.ValidationError):
            psm.deserialize(Model, '{"field": -1.9, "greeting": "hello"}')

        with self.assertRaises(psm.ValidationError):
            psm.deserialize(Model, '{"greeting": "hello"}')

    def test_deserialize_nonnullable(self):
        class Model(psm.SchemaModel):
            field = psm.FloatField(nullable=False)

        with self.assertRaises(psm.ValidationError):
            psm.deserialize(Model, '{"field": null}')

        m1 = psm.deserialize(Model, '{"field": 12.98}')
        self.assertEqual(12.98, m1.field)


class ListField_tests(unittest.TestCase):
    def test_validate_single_element_type(self):
        class Model(psm.SchemaModel):
            field = psm.ListField([psm.BoolField()], required=True)

        m1 = Model(field=[True, False, True, False, True, False, True, True, True, False])
        result, errors = m1.validate()
        self.assertTrue(result)
        self.assertEqual(0, len(errors))

        m2 = Model(field=[True, 'false'])
        multiple_types_result, multiple_types_errors = m2.validate()
        self.assertFalse(multiple_types_result)
        self.assertEqual(1, len(multiple_types_errors))

    def test_validate_multiple_element_types(self):
        class Model(psm.SchemaModel):
            field = psm.ListField([psm.BoolField(), psm.StringField(), psm.IntegerField(nullable=True)])

        m1 = Model(field=[True, 'Str', 10])
        m1_result, m1_errors = m1.validate()
        self.assertTrue(m1_result)
        self.assertEqual(0, len(m1_errors))

        m2 = Model(field=[True, 'Str', None])
        m2_result, m2_errors = m2.validate()
        self.assertTrue(m2_result)
        self.assertEqual(0, len(m2_errors))

        m3 = Model(field=[True, 'str', -1, 15])
        m3_result, m3_errors = m3.validate()
        self.assertFalse(m3_result)
        self.assertEqual(1, len(m3_errors))

        m4 = Model(field=[False, True, 1.2])
        m4_result, m4_errors = m4.validate()
        self.assertFalse(m4_result)
        self.assertGreaterEqual(len(m4_errors), 1)

    def test_validate_min_length(self):
        class Model(psm.SchemaModel):
            field = psm.ListField([psm.StringField()], min_length=1)

        m1 = Model(field=[])
        m1_result, m1_errors = m1.validate()
        self.assertFalse(m1_result)
        self.assertEqual(1, len(m1_errors))

        m2 = Model(field=['hello'])
        m2_result, m2_errors = m2.validate()
        self.assertTrue(m2_result)
        self.assertEqual(0, len(m2_errors))

        m3 = Model(field=['hello', 'goodbye'])
        m3_result, m3_errors = m3.validate()
        self.assertTrue(m3_result)
        self.assertEqual(0, len(m3_errors))

    def test_validate_max_length(self):
        class Model(psm.SchemaModel):
            field = psm.ListField([psm.IntegerField()], max_length=3)

        m1 = Model(field=[])
        m1_result, m1_errors = m1.validate()
        self.assertTrue(m1_result)
        self.assertEqual(0, len(m1_errors))

        m2 = Model(field=[1, 2, 3])
        m2_result, m2_errors = m2.validate()
        self.assertTrue(m2_result)
        self.assertEqual(0, len(m2_errors))

        m3 = Model(field = [1, 2, 3, 4])
        m3_result, m3_errors = m3.validate()
        self.assertFalse(m3_result)
        self.assertEqual(1, len(m3_errors))

    def test_validate_fixed_length(self):
        class Model(psm.SchemaModel):
            field = psm.ListField([psm.IntegerField()], min_length=2, max_length=2)

        m1 = Model(field=[0])
        m1_result, m1_errors = m1.validate()
        self.assertFalse(m1_result)
        self.assertEqual(1, len(m1_errors))

        m2 = Model(field=[0, 1])
        m2_result, m2_errors = m2.validate()
        self.assertTrue(m2_result)
        self.assertEqual(0, len(m2_errors))

        m3 = Model(field=[0, 1, 2])
        m3_result, m3_errors = m3.validate()
        self.assertFalse(m3_result)
        self.assertEqual(1, len(m3_errors))

    def test_validate_list_of_objects(self):
        class SubModel(psm.SchemaModel):
            data = psm.IntegerField()

        class Model(psm.SchemaModel):
            field = psm.ListField([psm.ObjectField(SubModel)])

        m1 = Model(field=[SubModel(data=1), SubModel(data=5)])
        m1_result, m1_errors = m1.validate()
        self.assertTrue(m1_result)
        self.assertEqual(0, len(m1_errors))

    def test_validate_list_of_lists(self):
        class Model(psm.SchemaModel):
            matrix = psm.ListField([psm.ListField([psm.IntegerField()])])

        m1 = Model(matrix=[[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        m1_result, m1_errors = m1.validate()
        self.assertTrue(m1_result)
        self.assertEqual(0, len(m1_errors))

    def test_validate_list_of_objects_with_list(self):
        class Transformation(psm.SchemaModel):
            offset = psm.ListField([psm.IntegerField()], min_length=3, max_length=3)

        class Model(psm.SchemaModel):
            transformations = psm.ListField([psm.ObjectField(Transformation)])

        m1 = Model(transformations=[Transformation(offset=[1, 1, 0]), Transformation(offset=[0, 1, 2])])
        m1_result, m1_errors = m1.validate()
        self.assertTrue(m1_result)
        self.assertEqual(0, len(m1_errors))

        m2 = Model(transformations=[Transformation(offset=[1, 1])])
        m2_result, m2_errors = m2.validate()
        self.assertFalse(m2_result)
        self.assertEqual(1, len(m2_errors))

    def test_serialize_list_of_integers(self):
        class Model(psm.SchemaModel):
            indices = psm.ListField([psm.IntegerField()])
        
        m1 = Model(indices=[1,8,9,101])
        m1_str = psm.serialize(m1)
        self.assertEqual('{"indices": [1, 8, 9, 101]}', m1_str)

    def test_serialize_list_of_lists(self):
        class Transformation(psm.SchemaModel):
            m = psm.ListField([ psm.ListField([psm.IntegerField()]) ])
        
        m1 = Transformation(m=[[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        m1_str = psm.serialize(m1)
        self.assertEqual('{"m": [[1, 0, 0], [0, 1, 0], [0, 0, 1]]}', m1_str)

    def test_serialize_list_of_objects(self):
        class Vector(psm.SchemaModel):
            x = psm.IntegerField(required=True, nullable=False)
            y = psm.IntegerField(required=True, nullable=False)
            z = psm.IntegerField(required=True, nullable=False)

        class Model(psm.SchemaModel):
            vectors = psm.ListField([psm.ObjectField(Vector)])

        m1 = Model(vectors=[Vector(x=1, y=0, z=0), Vector(x=0, y=1, z=0), Vector(x=0, y=0, z=1)])
        m1_str = psm.serialize(m1)
        self.assertEqual('{"vectors": [{"x": 1, "y": 0, "z": 0}, {"x": 0, "y": 1, "z": 0}, {"x": 0, "y": 0, "z": 1}]}', m1_str)

    def test_serialize_list_of_objects_with_list(self):
        class Vector(psm.SchemaModel):
            u = psm.ListField([psm.IntegerField()], min_length=3, max_length=3)

        class Model(psm.SchemaModel):
            vectors = psm.ListField([psm.ObjectField(Vector)])

        m1 = Model(vectors=[Vector(u=[1, 0, 0]), Vector(u=[0, 1, 0]), Vector(u=[0, 0, 1])])
        m1_str = psm.serialize(m1)
        self.assertEqual('{"vectors": [{"u": [1, 0, 0]}, {"u": [0, 1, 0]}, {"u": [0, 0, 1]}]}', m1_str)

    def test_serialize_mixed_list(self):
        class SubModel(psm.SchemaModel):
            data = psm.ListField([psm.BoolField()])

        class Model(psm.SchemaModel):
            bag = psm.ListField([
                psm.IntegerField(), 
                psm.ListField([psm.ObjectField(SubModel)])
            ])
        
        m1 = Model(bag=[
            1,
            [
                SubModel(data=[True, False]),
                SubModel(data=[True, True, False, False])
            ]
        ])
        m1_str = psm.serialize(m1)
        self.assertEqual('{"bag": [1, [{"data": [true, false]}, {"data": [true, true, false, false]}]]}', m1_str)
    
    def test_deserialize_list_of_integers(self):
        class Model(psm.SchemaModel):
            indices = psm.ListField([psm.IntegerField()])
        
        m1 = psm.deserialize(Model, '{"indices": [1, 8, 9, 101]}')
        self.assertIsInstance(m1, Model)
        self.assertIsInstance(m1.indices, list)
        expected = [1,8,9,101]
        self.assertEqual(len(m1.indices), len(expected))
        idx = 0
        while idx < len(expected):
            self.assertEqual(m1.indices[idx], expected[idx])
            idx = idx + 1
        
    def test_deserialize_list_of_lists(self):
        class Transformation(psm.SchemaModel):
            m = psm.ListField([ psm.ListField([psm.IntegerField()]) ])
        
        m1 = psm.deserialize(Transformation, '{"m": [[1, 0, 0], [0, 1, 0], [0, 0, 1]]}')
        expected = Transformation(m=[[1,0,0], [0,1,0], [0,0,1]])
        self.assertIsInstance(m1, Transformation)
        self.assertEqual(len(m1.m), len(expected.m))
        i = 0
        while i < len(m1.m):
            j = 0
            while j < len(m1.m[i]):
                self.assertEqual(m1.m[i], expected.m[i])
                j = j + 1
            i = i + 1

    def test_deserialize_list_of_objects(self):
        class Vector(psm.SchemaModel):
            x = psm.IntegerField(required=True, nullable=False)
            y = psm.IntegerField(required=True, nullable=False)
            z = psm.IntegerField(required=True, nullable=False)

        class Model(psm.SchemaModel):
            vectors = psm.ListField([psm.ObjectField(Vector)])

        m1 = psm.deserialize(Model, '{"vectors": [{"x": 1, "y": 0, "z": 0}, {"x": 0, "y": 1, "z": 0}, {"x": 0, "y": 0, "z": 1}]}')
        self.assertIsInstance(m1, Model)
        self.assertIsInstance(m1.vectors, list)
        self.assertEqual(len(m1.vectors), 3)
        for v in m1.vectors:
            self.assertIsInstance(v, Vector)
        
        self.assertTrue(m1.vectors[0].x == 1 and m1.vectors[0].y == 0 and m1.vectors[0].z == 0)
        self.assertTrue(m1.vectors[1].x == 0 and m1.vectors[1].y == 1 and m1.vectors[1].z == 0)
        self.assertTrue(m1.vectors[2].x == 0 and m1.vectors[2].y == 0 and m1.vectors[2].z == 1)

    def test_deserialize_list_of_objects_with_list(self):
        class Vector(psm.SchemaModel):
            u = psm.ListField([psm.IntegerField()], min_length=3, max_length=3)

        class Model(psm.SchemaModel):
            vectors = psm.ListField([psm.ObjectField(Vector)])

        m1 = psm.deserialize(Model, '{"vectors": [{"u": [1, 0, 0]}, {"u": [0, 1, 0]}, {"u": [0, 0, 1]}]}')
        expected = Model(vectors=[Vector(u=[1,0,0]), Vector(u=[0,1,0]), Vector(u=[0,0,1])])
        self.assertIsInstance(m1, Model)
        self.assertIsInstance(m1.vectors, list)
        self.assertEqual(len(m1.vectors), len(expected.vectors))
        i = 0
        while i < len(m1.vectors):
            self.assertIsInstance(m1.vectors[i], Vector)
            self.assertEqual(len(m1.vectors[i].u), 3)
            j = 0
            while j < len(m1.vectors[i].u):
                self.assertEqual(m1.vectors[i].u[j], expected.vectors[i].u[j])
                j = j + 1
            i = i + 1

    def test_deserialize_mixed_list(self):
        class SubModel(psm.SchemaModel):
            data = psm.ListField([psm.BoolField()])

        class Model(psm.SchemaModel):
            bag = psm.ListField([
                psm.IntegerField(), 
                psm.ListField([psm.ObjectField(SubModel)])
            ])
        
        m1 = psm.deserialize(Model, '{"bag": [1, [{"data": [true, false]}, {"data": [true, true, false]}]]}')
        self.assertIsInstance(m1, Model)
        self.assertIsInstance(m1.bag, list)
        self.assertIsInstance(m1.bag[0], int)
        self.assertEqual(m1.bag[0], 1)
        self.assertIsInstance(m1.bag[1], list)
        self.assertEqual(len(m1.bag[1]), 2)
        for i in m1.bag[1]:
            self.assertIsInstance(i, SubModel)
            self.assertIsInstance(i.data, list)

        self.assertEqual(len(m1.bag[1][0].data), 2)
        self.assertEqual(m1.bag[1][0].data[0], True)
        self.assertEqual(m1.bag[1][0].data[1], False)

        self.assertEqual(len(m1.bag[1][1].data), 3)
        self.assertEqual(m1.bag[1][1].data[0], True)
        self.assertEqual(m1.bag[1][1].data[1], True)
        self.assertEqual(m1.bag[1][1].data[2], False)

    def test_deserialize_mixed_list_mismatched_length(self):
        class Model(psm.SchemaModel):
            bag = psm.ListField([psm.IntegerField(), psm.BoolField()])
        
        m1 = Model(bag=[1, False, 'str'])
        with self.assertRaises(TypeError):
            psm.deserialize(Model, m1)

class ObjectField_tests(unittest.TestCase):
    def test_validation_obj_of_obj(self):
        class Model1(psm.SchemaModel):
            field = psm.StringField()

        class Model2(psm.SchemaModel):
            obj_field = psm.ObjectField(Model1)

        m1 = Model2(obj_field=Model1(field='greeting'))
        m1_result, m1_errors = m1.validate()
        self.assertTrue(m1_result)
        self.assertEqual(0, len(m1_errors))

        class Model3(psm.SchemaModel):
            field = psm.StringField()

        m2 = Model2(obj_field=Model3(field='greeting'))
        m2_result, m2_errors = m2.validate()
        self.assertFalse(m2_result)
        self.assertEqual(1, len(m2_errors))

        m3 = Model3(obj_field='greeting')
        m3_result, m3_errors = m3.validate()
        self.assertFalse(m3_result)
        self.assertEqual(1, len(m3_errors))

    def test_serialize_obj_of_objs(self):
        class SubModel(psm.SchemaModel):
            field = psm.StringField()

        class Model(psm.SchemaModel):
            obj_field = psm.ObjectField(SubModel)

        m1 = Model(obj_field=SubModel(field='greetings'))
        m1_str = psm.serialize(m1)
        self.assertEqual('{"obj_field": {"field": "greetings"}}', m1_str)

    def test_deserialize_obj_of_objs(self):
        class SubModel(psm.SchemaModel):
            field = psm.StringField()

        class Model(psm.SchemaModel):
            obj_field = psm.ObjectField(SubModel)

        m1 = psm.deserialize(Model, '{"obj_field": {"field": "greetings"}}')
        self.assertIsInstance(m1, Model)
        self.assertIsInstance(m1.obj_field, SubModel)
        self.assertEqual(m1.obj_field.field, 'greetings')

if __name__ == '__main__':
    unittest.main()
