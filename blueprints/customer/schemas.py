from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from ...models import Customer

class CustomerSchema(SQLAlchemySchema):
    class Meta:
        model = Customer
        load_instance = True

    id = auto_field(dump_only=True)
    name = auto_field(required=True)
    email = auto_field(required=True)
    password = auto_field(required=True)
    phone_number = auto_field()
    address = auto_field()

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
