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

Warning: do not define **__init__** on any child classes of **SchemaModel** as the module relies on these classes being instantiated with an empty constructor, particularly when deserializing a model from a json string.

## Data Fields

- Applying **required** to a **DataField** instance will cause validation to fail if said **DataField** is absent.
- Applying **nullable** to a **DataField** instance will permit **None** as a valid value in addition to its defined type.

### BoolField(required=False, nullable=False)

``` Python
class Model(SchemaModel):
    a_nullable_bool = BoolField(required=True, nullable=True)

m1 = Model(a_nullable_bool=None)
is_valid, errors = m1.validate()
print(is_valid, errors)
# True, []

m2 = Model()
is_valid, erros = m2.validate()
print(is_valid, errors)
# False, ['DataField "a_nullable_bool" is required']
```

### IntegerField(required=False, nullable=False, _min=IntMin, _max=IntMax, allowed=[], forbidden=[])

``` Python
class Model(SchemaModel):
    small_prime = IntegerField(allowed=[1, 2, 3, 5, 7])

m1 = Model(small_prime=4)
is_valid, errors = m1.validate()
print(is_valid, errors)
# False, ['Value "4" not permitted in DataField "small_prime"']

m2 = Model(small_prime=5)
is_valid, errors = m2.validate()
print(is_valid, errors)
# True, []
```

### FloatField(required=False, nullable=False, _min=FloatMin, _max=FloatMax, allowed=[], forbidden=[])

``` Python
class Model(SchemaModel):
    real = FloatField(_min=-1.0, _max=1.0)

m1 = Model(real=-1.1)
is_valid, errors = m1.validate()
print(is_valid, errors)
# False, ['Value "-1.1" out of bounds for DataField "real"']

m2 = Model(real=0.0)
is_valid, errors = m1.validate()
print(is_valid, errors)
# True, []
```

### StringField(required=False, nullable=False, allowed=[], forbidden=[])

``` Python
class Model(SchemaModel):
    s = StringField(forbidden=['love', 'fruit'])

m1 = Model(s='love')
is_valid, errors = m1.validate()
print(is_valid, errors)
# False, ['Value "love" is not permitted for DataField "s"']

m2 = Model(s='chocolate')
is_valid, errors = m2.validate()
print(is_valid, errors)
# True, []
```

### ListField(type_mapping, required=False, nullable=False, min_length=0, max_length=IntMax)
    
- **type_mapping** expects an array of **DataField** objects
    - when a list has a single element type there should only be the corresponding **DataField** type in the **type_mapping** list

    ``` Python
    class Model(SchemaModel):
        data = ListField(type_mapping=[IntegerField()])

    m1 = Model(data=[1, 2, 3, 4, 5, 6])
    is_valid, errors = m1.validate()
    print(is_valid, errors)
    # True, []
    ```
    
    - when a list has mixed element types the length of the list on the model must be the same length as the number of mixed types
    
    ``` Python
    class Model(SchemaModel):
        data = ListField(type_mapping=[IntegerField(), StringField()])

    m1 = Model(data=[10, 'goodbye'])
    is_valid, errors = m1.validate()
    print(is_valid, errors)
    # True, []

    m2 = Model(data=[1, 'hello', True])
    is_valid, errors = m1.validate()
    print(is_valid, errors)
    # False, ['type_mapping mismatch DataField "data"']
    ```

### ObjectField(cls, required=False, nullable=False)

- The **ObjectField** is needed for defining Objects within Objects schemas
- **cls** defines the class that an instance will be checked against in the schema

``` Python
class Vector(SchemaModel):
    x = IntegerField()
    y = IntegerField()
    z = IntegerField()

class Matrix(SchemaModel):
    vectors = ObjectField(Vector)

m1 = Matrix(vectors=[Vector(1,0,0), Vector(0, 1, 0), Vector(0, 0, 1)])
is_valid, errors = m1.validate()
print(is_valid, errors)
# True, []
```

## Work In Progress

- Clean up the code: psm.py and tests.py
- Improve error messages
- Add custom function validation on any given DataField
- Maybe add a DictField? or LongField?

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
