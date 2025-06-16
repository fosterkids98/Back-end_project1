from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from ...models import Ticket
from datetime import timezone
from ...extensions import ma
from body_shop.blueprints.inventory.schemas import InventorySchema
from body_shop.blueprints.mechanic.schemas import MechanicLiteSchema

class PartQuantitySchema(ma.Schema):
    part = fields.Nested(InventorySchema)
    quantity = fields.Int()

class TicketSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Ticket
        load_instance = True

    status = ma.auto_field()
    customer_id = ma.auto_field()
    mechanics = fields.Nested(MechanicLiteSchema, many=True)
    service_date = ma.auto_field(dump_default=lambda: timezone.now())
    parts = fields.Nested(PartQuantitySchema, many=True)
    total_cost = ma.auto_field(dump_default=0.0)

ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)