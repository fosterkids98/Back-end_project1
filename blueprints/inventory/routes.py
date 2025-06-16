from . import inventory_bp
from ...models import Inventory
from ...extensions import db
from .schemas import inventory_schema, inventories_schema
from ...utils.util import mechanic_required
from flask import request 

@inventory_bp.route('/', methods=['POST'])
@mechanic_required
def create_part(current_mechanic_id=None):
    data = request.get_json()

    if isinstance(data, list):
        # Load multiple parts
        parts = inventories_schema.load(data, session=db.session)
        db.session.add_all(parts)
        db.session.commit()
        return inventories_schema.dump(parts), 201

    elif isinstance(data, dict):
        # Load single part
        part = inventory_schema.load(data, session=db.session)
        db.session.add(part)
        db.session.commit()
        return inventory_schema.dump(part), 201

    else:
        return {"error": "Invalid data format. Expected a JSON object or list."}, 400


@inventory_bp.route('/', methods=['GET'])
def get_parts():
    return inventories_schema.dump(Inventory.query.all()), 200

@inventory_bp.route('/<int:id>', methods=['GET'])
def get_part(id):
    return inventory_schema.dump(Inventory.query.get_or_404(id)), 200

@inventory_bp.route('/<int:id>', methods=['PUT'])
@mechanic_required
def update_part(id, current_mechanic_id=None):
    part = Inventory.query.get_or_404(id)
    part = inventory_schema.load(request.json, instance=part, partial=True, session=db.session)
    db.session.commit()
    return inventory_schema.dump(part), 200

@inventory_bp.route('/<int:id>', methods=['DELETE'])
@mechanic_required
def delete_part(id, current_mechanic_id=None):
    part = Inventory.query.get_or_404(id)
    db.session.delete(part); db.session.commit()
    return '', 204
