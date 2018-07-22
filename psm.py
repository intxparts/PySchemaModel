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

    def _check_nullable(self, name, v):
        errors = []
        result = True

        if self.nullable and v == None:
            return result, errors

        if not self.nullable and v == None:
            result = False
            errors.append(str.format('Field "{}" is not nullable', name))
        
        return result, errors

    def _check_permitted(self, name, v):
        errors = []
        result = True

        if (len(self.allowed) > 0 and not v in self.allowed) or (len(self.forbidden) > 0 and v in self.forbidden):
            result = False
            errors.append(str.format('Field "{}" is not a permitted value', name))

        return result, errors

    def _check_instance(self, name, v):
        return True, []

    def is_valid(self, name, v):
        null_check, null_check_errors = self._check_nullable(name, v)
        if not null_check:
            return null_check, null_check_errors

        errors = []
        result = True

        instance_check, instance_check_errors = self._check_instance(name, v)
        if not instance_check:
            result = False
            errors.extend(instance_check_errors)

        permitted_check, permitted_check_errors = self._check_permitted(name, v)
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

    def _check_permitted(self, name, v):
        return True, []

    def _check_instance(self, name, v):
        errors = []
        result = True

        if not isinstance(v, bool):
            result = False
            errors.append(str.format('Field "{}" must be a bool', name))
        return result, errors

class StringField(DataField):
    def __init__(
        self,
        required = False,
        nullable = False,
        allowed = [],
        forbidden = []
    ):
        super().__init__(required, nullable, allowed, forbidden)
    
    def _check_instance(self, v):
        errors = []
        result = True

        if not isinstance(v, str):
            result = False
            errors.append(str.format('Field "{}" must be a str', name))
        return result, errors


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
    
    def _check_instance(self, name, v):
        errors = []
        result = True
        if not isinstance(v, int):
            result = False
            errors.append(str.format('Field "{}" must be a int', name))
            return result, errors
        
        if self.min > v or self.max < v:
            result = False
            errors.append(str.format('Value out of bounds: {}. Field "{}" must be within bounds [{}, {}]', v, name, self.min, self.max))

        return result, errors

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
    
    def _check_instance(self, name, v):
        errors = []
        result = True
        if not isinstance(v, float):
            result = False
            errors.append(str.format('Field "{}" must be a float', name))
            return result, errors
        
        if self.min > v or self.max < v:
            result = False
            errors.append(str.format('Value out of bounds: {}. Field "{}" must be within bounds [{}, {}]', v, name, self.min, self.max))

        return result, errors

class ListField(DataField):
    def __init__(
        self,
        type_mapping,
        required = False,
        nullable = False,
        allowed = [],
        forbidden = [],
        min_length = 0,
        max_length = _MAX_INT
    ):
        super().__init__(required, nullable, allowed, forbidden)
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

    def _check_instance(self, name, v):
        errors = []
        result = True

        if not isinstance(v, list):
            result = False
            errors.append(str.format('Field "{}" must be a list', name))
            return result, errors

        if len(type_mapping) == 1:
            for i in v:
                if not isinstance(i, type_mapping[0]):
                    result = False
                    errors.append(str.format('invalid type: {}, expected: {} for Field "{}"', type(i).__name__, type_mapping[0].__name__, name))
        else:
            idx = 0
            for i in v:
                if not isinstance(i, type_mapping[idx]):
                    result = False
                    errors.append(str.format('invalid type: {}, expected: {} for Field "{}"', type(i).__name__, type_mapping[0].__name__, name))
                idx = idx + 1

        if len(v) > self.max_length:
            result = False
            errors.append(str.format('List Field "{}" exceeded its maximum length: {}, with length: {}', name, self.max_length, len(v)))
        if len(v) < self.min_length:
            result = False
            errors.append(str.format('List Field "{}" does not satisfy the length requirement: {}, with length: {}', name, self.min_length, len(v)))

        return result, errors

class DictField(DataField):
    def __init__(
        self,
        key_type,
        value_type,
        required = False,
        nullable = False
    ):
        super().__init__(required, nullable)
        self.key_type = key_type
        self.value_type = value_type
    
    def _check_instance(self, name, value):
        errors = []
        result = True

        if not isinstance(value, dict):
            result = True
            errors.append(str.format('Field "{}" must be a dict', name))
            return result, errors

        for k, v in value.items():
            if not isinstance(k, self.key_type):
                result = False
                errors.append(str.format('key type: {} for Field "{}" must be of type: {}', type(k).__name__, name, type(key_type).__name__))
            if not isinstance(v, self.value_type):
                result = False
                errors.append(str.format('value type: {} for Field "{}" must be of type: {}', type(v).__name__, name, type(value_type).__name__))

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

    def _check_instance(self, name, v):
        errors = []
        result = True
        if not isinstance(v, self.cls):
            result = False
            errors.append(str.format('Field "{}" must be of type: {}', name, self.cls.__name__))
            return result, errors

        subresult, suberrors = v.validate()
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

    def to_json_obj(self):
        d = {}
        for k, v in self.__dict__.items():
            if isinstance(v, SchemaModel):
                d[k] = v.to_json_obj()
            else:
                d[k] = v
        return d

    def validate(self):
        result = True
        errors = []
        schema = getattr(self, '__schema')
        keys = self.__dict__.keys()
        for k, v in schema.items():
            if k in keys:
                if not v.nullable and self.__dict__[k] == None:
                    errors.append(str.format('field is not nullable: {}', k))
                    result = False
                
                subresult, suberrors = v.is_valid(k, self.__dict__[k])
                if not subresult:
                    result = False
                    errors.extend(suberrors)

            else:
                if v.required:
                    errors.append(str.format('required field is missing: {}', k))
                    result = False
        allow_unknowns = getattr(self, '__allow_unknowns')
        if allow_unknowns:
            schema_keys = schema.keys()
            for k in keys:
                if not k in schema_keys:
                    errors.append(str.format('unknown fields not permitted, attribute must be defined in schema: {}', k))

        return result, errors

def serialize(obj):
    if not isinstance(obj, SchemaModel):
        raise TypeError("Object must be an instance of a SchemaModel")
    result, errors = obj.validate()
    if not result:
        raise ValidationError(errors)
    return json.dumps(obj.to_json_obj())


def _instantiate_class(cls, d):
    obj = cls()
    schema = getattr(cls, '__schema')
    for k, v in schema.items():
        if k in d:
            if isinstance(v, ObjectField):
                obj.__dict__[k] = _instantiate_class(v.cls, d[k])
            else:
                obj.__dict__[k] = d[k]
    return obj

def deserialize(cls, json_string):
    if not issubclass(cls, SchemaModel):
        raise TypeError("Class must be a subclass of SchemaModel")
    d = json.loads(json_string)
    # create an instance of the given class
    # populate that instance with the data from the json dict
    obj = _instantiate_class(cls, d)

    result, errors = obj.validate()
    if not result:
        raise ValidationError(errors)
    return obj

