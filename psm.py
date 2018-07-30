import json
import sys

_MAX_INT = sys.maxsize
_MIN_INT = -sys.maxsize - 1

def _is_builtin_name(s):
    if not isinstance(s, str):
        return False
    if len(s) > 4 and s[0] == '_' and s[1] == '_' and s[-1] == '_' and s[-2] == '_':
        return True
    return False


class DataField:
    def __init__(
        self,
        required = False,
        nullable = False,
        allowed = [],
        forbidden = []
    ):
        self.required = required
        self.nullable = nullable
        self.allowed = allowed
        self.forbidden = forbidden

    def _check_permitted(self, name, value):
        if (len(self.allowed) > 0 and not value in self.allowed) or (len(self.forbidden) > 0 and value in self.forbidden):
            return False, [str.format('Field "{}" is not a permitted value', name)]
        return True, []

    def _check_instance(self, name, value):
        return True, []

    def is_valid(self, name, value):
        if self.nullable and value == None:
            return True, []

        if not self.nullable and value == None:
            return False, [str.format('Field "{}" is not nullable', name)]

        errors = []
        result = True

        instance_check, instance_check_errors = self._check_instance(name, value)
        if not instance_check:
            result = False
            errors.extend(instance_check_errors)

        permitted_check, permitted_check_errors = self._check_permitted(name, value)
        if not permitted_check:
            result = False
            errors.extend(permitted_check_errors)

        return result, errors

class BoolField(DataField):
    def __init__(self,
        required = False,
        nullable = False
    ):
        super().__init__(required, nullable)

    def _check_permitted(self, name, value):
        return True, []

    def _check_instance(self, name, value):
        if not isinstance(value, bool):
            return False, [str.format('Field "{}" must be a bool', name)]
        return True, []

class StringField(DataField):
    def __init__(
        self,
        required = False,
        nullable = False,
        allowed = [],
        forbidden = []
    ):
        super().__init__(required, nullable, allowed, forbidden)

    def _check_instance(self, name, value):
        if not isinstance(value, str):
            return False, [str.format('Field "{}" must be a str', name)]
        return True, []


class IntegerField(DataField):
    def __init__(
        self,
        required = False,
        nullable = False,
        allowed = [],
        forbidden = [],
        _min = _MIN_INT,
        _max = _MAX_INT
    ):
        super().__init__(required, nullable, allowed, forbidden)
        self.min = _min
        self.max = _max

    def _check_instance(self, name, value):
        if not isinstance(value, int):
            return False, [str.format('Field "{}" must be a int', name)]

        if self.min > value or self.max < value:
            return False, [str.format('Value out of bounds: {}. Field "{}" must be within bounds [{}, {}]', value, name, self.min, self.max)]

        return True, []

class FloatField(DataField):
    def __init__(
        self,
        required = False,
        nullable = False,
        allowed = [],
        forbidden = [],
        _min = _MIN_INT,
        _max = _MAX_INT
    ):
        super().__init__(required, nullable, allowed, forbidden)
        self.min = _min
        self.max = _max

    def _check_instance(self, name, value):
        errors = []
        result = True
        if not isinstance(value, float):
            result = False
            errors.append(str.format('Field "{}" must be a float', name))
            return result, errors

        if self.min > value or self.max < value:
            result = False
            errors.append(str.format('Value out of bounds: {}. Field "{}" must be within bounds [{}, {}]', value, name, self.min, self.max))

        return result, errors

class ListField(DataField):
    def __init__(
        self,
        type_mapping,
        required = False,
        nullable = False,
        min_length = 0,
        max_length = _MAX_INT
    ):
        super().__init__(required, nullable)
        if not isinstance(type_mapping, list):
            raise TypeError('"type_mapping" must be a list of data field types')
        if len(type_mapping) == 0:
            raise ValueError('"type_mapping" requires at least one data field type to define its elements')
        for t in type_mapping:
            if not isinstance(t, DataField):
                raise TypeError(str.format('invalid type: {}, provided for "type_mapping", type must derive from DataField', type(t)))
        self.type_mapping = type_mapping
        self.min_length = min_length
        self.max_length = max_length

    def _check_permitted(self, name, value):
        return True, []

    def _check_instance(self, name, value):

        if not isinstance(value, list):
            return False, [str.format('Field "{}" must be a list', name)]

        errors = []
        result = True

        if len(self.type_mapping) == 1:
            for i in value:
                subresult, suberrors = self.type_mapping[0].is_valid(name, i)
                if not subresult:
                    result = False
                    errors.append(str.format('invalid type: {}, expected: {} for Field "{}"', type(i).__name__, type(self.type_mapping[0]).__name__, name))
        else:
            if len(value) != len(self.type_mapping):
                return False, [str.format('List Field "{}" length mismatch between schema and value', name)]
            idx = 0
            for i in value:
                subresult, suberrors = self.type_mapping[idx].is_valid(name, i)
                if not subresult:
                    result = False
                    errors.append(str.format('invalid type: {}, expected: {} for Field "{}"', type(i).__name__, type(self.type_mapping[idx]).__name__, name))
                idx = idx + 1

        if len(value) > self.max_length:
            result = False
            errors.append(str.format('List Field "{}" exceeded its maximum length: {}, with length: {}', name, self.max_length, len(value)))
        if len(value) < self.min_length:
            result = False
            errors.append(str.format('List Field "{}" does not satisfy the length requirement: {}, with length: {}', name, self.min_length, len(value)))

        return result, errors

class ObjectField(DataField):
    def __init__(
        self,
        cls,
        required = False,
        nullable = False
    ):
        super().__init__(required, nullable)
        self.cls = cls

    def _check_instance(self, name, value):
        if not isinstance(value, self.cls):
            return False, [str.format('Field "{}" must be of type: {}', name, self.cls.__name__)]

        errors = []
        result = True
        subresult, suberrors = value.validate()
        if not subresult:
            result = False
            errors.extend(suberrors)

        return result, errors

class ValidationError(Exception):
    def __init__(self, validation_errors):
        self.errors = validation_errors


class Schema(type):
    def __new__(metaclass, metaclass_name, bases, namespace, **options):
        new_namespace = {}
        new_namespace['__schema'] = {}
        new_namespace['__allow_unknowns'] = options.get('allow_unknowns', False)
        for k, v in namespace.items():
            if not _is_builtin_name(k):
                if isinstance(v, DataField):
                    new_namespace['__schema'][k] = v
                else:
                    new_namespace[k] = v
            else:
                new_namespace[k] = v
        return super().__new__(metaclass, metaclass_name, bases, new_namespace)

    def __init__(cls, cls_name, bases, namespace, **options):
        super().__init__(cls_name, bases, namespace)

class SchemaModel(metaclass=Schema, allow_unknowns=False):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def _list_to_json_obj(self, v):
        list_of_models = []
        for i in v:
            if isinstance(i, SchemaModel):
                list_of_models.append(i.to_json_obj())
            elif isinstance(i, list):
                list_of_models.append(self._list_to_json_obj(i))
            else:
                list_of_models.append(i)
        return list_of_models

    def to_json_obj(self):
        d = {}
        for k, v in self.__dict__.items():
            if isinstance(v, SchemaModel):
                d[k] = v.to_json_obj()
            elif isinstance(v, list):
                d[k] = self._list_to_json_obj(v)
            else:
                d[k] = v
        return d

    def validate(self):
        result = True
        errors = []
        schema = getattr(self, '__schema')
        instance_attr_names = self.__dict__.keys()
        for k, v in schema.items():
            if k in instance_attr_names:
                subresult, suberrors = v.is_valid(k, self.__dict__[k])
                if not subresult:
                    result = False
                    errors.extend(suberrors)
            else:
                if v.required:
                    result = False
                    errors.append(str.format('required field is missing: {}', k))
        allow_unknowns = getattr(self, '__allow_unknowns')
        if not allow_unknowns:
            schema_keys = schema.keys()
            for attr_name in instance_attr_names:
                if not attr_name in schema_keys:
                    result = False
                    errors.append(str.format('unknown fields not permitted, attribute must be defined in schema: {}', k))

        return result, errors

def serialize(obj):
    if not isinstance(obj, SchemaModel):
        raise TypeError("Object must be an instance of a SchemaModel")
    result, errors = obj.validate()
    if not result:
        raise ValidationError(errors)
    return json.dumps(obj.to_json_obj())

def _instantiate_list_field(list_schema_obj, list_obj):
    populated_list = []
    if len(list_schema_obj.type_mapping) == 1:
        for item in list_obj:
            if isinstance(list_schema_obj.type_mapping[0], ObjectField):
                populated_list.append(
                    _instantiate_obj_field(
                        list_schema_obj.type_mapping[0].cls,
                        item
                    )
                )
            elif isinstance(list_schema_obj.type_mapping[0], ListField):
                populated_list.append(
                    _instantiate_list_field(
                        list_schema_obj.type_mapping[0],
                        item
                    )
                )
            else:
                populated_list.append(item)
    else:
        # multiple types for the list, fixed length
        if len(list_schema_obj.type_mapping) != len(list_obj):
            raise TypeError('list does not match the defined ListField\'s type_mapping schema')
        
        idx = 0
        for type_obj in list_schema_obj.type_mapping:
            if isinstance(type_obj, ObjectField):
                populated_list.append(
                    _instantiate_obj_field(
                        type_obj.cls,
                        list_obj[idx]
                    )
                )
            elif isinstance(type_obj, ListField):
                populated_list.append(
                    _instantiate_list_field(
                        type_obj,
                        list_obj[idx]
                    )
                )
            else:
                populated_list.append(list_obj[idx])
            idx = idx + 1
    return populated_list    

def _instantiate_obj_field(cls, data_dict):
    obj = cls()
    schema = getattr(cls, '__schema')
    for schema_key, schema_obj in schema.items():
        if schema_key in data_dict:
            if isinstance(schema_obj, ObjectField):
                obj.__dict__[schema_key] = _instantiate_obj_field(
                    schema_obj.cls,
                    data_dict[schema_key]
                )
            elif isinstance(schema_obj, ListField):
                obj.__dict__[schema_key] = _instantiate_list_field(
                    schema_obj,
                    data_dict[schema_key]
                )
            else:
                obj.__dict__[schema_key] = data_dict[schema_key]
    instance_keys = obj.__dict__.keys()

    # load the remaining dictionary items into the class
    for k, v in data_dict.items():
        if not k in instance_keys:
            obj.__dict__[k] = v
    return obj

def deserialize(cls, json_string):
    if not issubclass(cls, SchemaModel):
        raise TypeError("Class must be a subclass of SchemaModel")
    d = json.loads(json_string)
    # create an instance of the given class
    # populate that instance with the data from the json dict
    obj = _instantiate_obj_field(cls, d)
    result, errors = obj.validate()
    if not result:
        raise ValidationError(errors)
    return obj
