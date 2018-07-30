# PySchemaModel

A python module to provide a class based approach for defining JSON schemas with built-in validation and serialization. 

- Supported Python versions: 3.6+

## Install

The psm.py file should be dropped into an existing project and imported by it.

## Usage

Define a class that extends **SchemaModel** and use the classes that extend **DataField** to define the schema's fields by declaring class level attributes on the model. 

The following **DataField** classes have been provided to help define schemas. 

- IntegerField
- FloatField
- BoolField
- StringField
- ListField
- ObjectField

### Defining the model
``` Python
from psm import *

class User(SchemaModel):
    email = StringField()
    age = IntegerField()
```

### Validating an instance of a model
``` Python
# create an instance of the model
valid_user = User(email='john.doe@doetech.com', age=45)

# validate the instance against the defined schema
is_valid, error_list = valid_user.validate()
print(is_valid)
# True 
print(error_list)
# []

# email should be a string but is an int
invalid_user = User(email=123, age=45)
is_valid, error_list = invalid_user.validate()
print(is_valid)
# False
print(error_list)
# ['DataField "email" must be of type "str"']
```

### Serializing an instance of a model
``` Python
user_json_str = serialize(User(email='john.doe@doetech.com', age=45))
print(user_json_str)
# {"email": "john.doe@doetech.com", "age": 45}
```

### Deserializing a model from a json string
``` Python
u = deserialize(User, '{"email": "john.doe@doetech.com", "age": 45}')
print(isinstance(u, User))
# True
print(u.email, u.age)
# john.doe@doetech.com    45
```

## How the module works

When creating a class that extends **SchemaModel**, the class will be generated with an additional attribute named **__schema**. This attribute is a **dict** populated with the **DataField**'s defined as class level attributes on the child class of **SchemaModel**.

The attribute **__schema** should not be tampered with as it stores the schema information to validate any given instance of the model against. Modifying this attribute could cause this modules features to improperly function.

Validation is automatically performed during serialization/deserialization for any instance against it's defined schema. If the validation fails, it is raised as a **ValidationError**.

## Data Fields

### BoolField

Required parameters:

    - None

Optional parameters:

    - required
    - nullable

### IntegerField

Required parameters:

    - None

Optional parameters:

    - required
    - nullable
    - _min
    - _max
    - allowed
    - forbidden

### FloatField

Required parameters:

    - None

Optional parameters:

    - required
    - nullable
    - _min
    - _max
    - allowed
    - forbidden

### StringField

Required parameters:

    - None

Optional parameters:

    - required
    - nullable
    - allowed
    - forbidden

### ListField

Required parameters:

    - type_mapping

Optional parameters:

    - required
    - nullable
    - min_length
    - max_length

### ObjectField

Required parameters:

    - cls

Optional parameters:

    - required
    - nullable


## License

MIT License

Copyright (c) 2018 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
