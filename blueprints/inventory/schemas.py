from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ...models import Inventory
from ...extensions import ma

class InventorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        load_instance = True
        include_relationships = True
        include_fk = True


inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)