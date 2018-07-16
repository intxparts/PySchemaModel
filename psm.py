import cerberus
import json

def is_builtin_name(s):
    if not isinstance(s, str):
        return False
    if len(s) > 4 and s[0] == '_' and s[1] == '_' and s[-1] == '_' and s[-2] == '_':
        return True
    return False


class CerberusValidationError(Exception):
    def __init__(self, validation_errors):
        self.errors = validation_errors


class Schema(type):
    def __new__(metaclass, metaclass_name, bases, namespace):
        new_namespace = {}
        new_namespace['__schema'] = {}
        for k, v in namespace.items():
            if not is_builtin_name(k) and isinstance(v, dict): # expects a cerberus dict
                new_namespace['__schema'][k] = v
            else:
                new_namespace[k] = v

        return super().__new__(metaclass, metaclass_name, bases, new_namespace)

    def __init__(cls, cls_name, bases, namespace):
        super().__init__(cls_name, bases, namespace)


class SchemaModel(metaclass=Schema):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __setattr__(self, attr, value):
        schema = getattr(self, '__schema')
        for k in schema.keys():
            if k == attr:
                self.__dict__[attr] = value
                return
        raise AttributeError(str.format("Attribute not defined in schema: {}", attr))

    def validate(self):
        schema = getattr(self, '__schema')
        v = cerberus.Validator(schema)
        result = v.validate(vars(self))
        errors = v._errors
        return result, errors


def serialize(obj):
    if not isinstance(obj, SchemaModel):
        raise TypeError("Object must be an instance of a SchemaModel")
    result, errors = obj.validate()
    if not result:
        raise CerberusValidationError(errors)
    return json.dumps(vars(obj))


def deserialize(cls, json_string):
    if not issubclass(cls, SchemaModel):
        raise TypeError("Class must be a subclass of SchemaModel")
    d = json.loads(json_string)
    # create an instance of the given class
    # populate that instance with the data from the json dict
    obj = cls(**d)

    result, errors = obj.validate()
    if not result:
        raise CerberusValidationError(errors)
    return obj

