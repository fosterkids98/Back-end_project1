from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from ...models import Mechanic


class MechanicSchema(SQLAlchemySchema):
    class Meta:
        model = Mechanic
        load_instance = True

    id = auto_field(dump_only=True)
    name = auto_field(required=True)
    email = auto_field(required=True)
    password = auto_field(required=True)
    phone = auto_field()
    salary = auto_field()

class MechanicLiteSchema(SQLAlchemySchema):
    class Meta:
        model = Mechanic
        load_instance = True
    id = auto_field(dump_only=True)
    name = auto_field(required=True)

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)

