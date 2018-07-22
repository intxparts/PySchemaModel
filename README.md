# PySchemaModel

A python module to provide a class based approach to define JSON schemas with built-in validation and serialization. 


```python

from psm import *

class User(SchemaModel):
    email = StringField(required=True, nullable=False)
    age = IntegerField(required=True, nullable=False, _min=0, _max=150)


class Payload(SchemaModel):
    user = ObjectField(User, required=True, nullable=True)
    is_active = BoolField(required=False, nullable=True)


person1 = User(email='user1@someco.com', age=27)
result, errors = person.validate()
#    [> (True, [])

person1_str = serialize(person1)
#    [> '{ "email": "user1@someco.com", "age": 27 }'

person2 = User(email='user2@anotherco.com')
result, errors = person2.validate()
#    [> (False, ['age is a required field']) 

person2_str = serialize(person2)
#    [> Attribute error: required field missing: "age"

payload = Payload(user=person1, is_active=False)
result, errors = payload.validate()
#    [> (True, [])

payload_str = serialize(payload)
#    [> '{ "user": { "email": "user1@someco.com", "age": 27 }, "is_active": false }'

payload_deserialized = deserialize(Payload, payload_str)
#    [> <class __main__.Payload>


```