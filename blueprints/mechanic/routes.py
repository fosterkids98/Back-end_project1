from flask import request, jsonify, abort
from . import mechanic_bp
from ...models import Mechanic, Ticket
from ...extensions import db
from .schemas import mechanic_schema, mechanics_schema
from ...utils.util import encode_mechanic_token, mechanic_required


@mechanic_bp.route('/by-tickets', methods=['GET'])
@mechanic_required
def mechanics_by_ticket_count(current_mechanic_id=None):
    results = (
        db.session.query(Mechanic, db.func.count(Ticket.id).label('ticket_count'))
        .join(Ticket.mechanic)
        .group_by(Mechanic.id)
        .order_by(db.desc('ticket_count'))
        .all()
    )
    return jsonify([{
        'id': m.id, 'name': m.name, 'ticket_count': tc
    } for m, tc in results]), 200


@mechanic_bp.route('/login', methods=['POST'])
def mechanic_login():
    data = request.json
    mech = Mechanic.query.filter_by(email=data['email'], password=data['password']).first()
    if not mech:
        return jsonify({'error': 'Invalid credentials'}), 401
    mechanic_token = encode_mechanic_token(mech.id)
    return jsonify({'mechanic_token': mechanic_token}), 200


@mechanic_bp.route('/', methods=['GET'])
@mechanic_required
def get_mechanics(current_mechanic_id=None):
    return jsonify(mechanics_schema.dump(Mechanic.query.all()))

@mechanic_bp.route('/', methods=['POST'])
def create_mechanic():
    data = request.get_json()

    if isinstance(data, list):
        # Bulk create
        mechanics = mechanics_schema.load(data, session=db.session)
        db.session.add_all(mechanics)
        db.session.commit()
        return mechanics_schema.dump(mechanics), 201

    elif isinstance(data, dict):
        # Single create
        new_mechanic = mechanic_schema.load(data, session=db.session)
        db.session.add(new_mechanic)
        db.session.commit()
        return mechanic_schema.dump(new_mechanic), 201

    else:
        return {"error": "Invalid data format. Expected a JSON object or list."}, 400

@mechanic_bp.route('/<int:mechanic_id>', methods=['PUT'])
@mechanic_required
def update_mechanic(mechanic_id, current_mechanic_id=None):
    mechanic = Mechanic.query.get_or_404(mechanic_id)
    updated_mechanic = mechanic_schema.load(request.json, instance=mechanic, partial=True, session=db.session)
    db.session.commit()
    return mechanic_schema.dump(updated_mechanic)

@mechanic_bp.route('/<int:id>', methods=['DELETE'])
@mechanic_required
def delete_mechanic(id, current_mechanic_id=None):
    mechanic = Mechanic.query.get_or_404(id)
    db.session.delete(mechanic)
    db.session.commit()
    return '', 204
