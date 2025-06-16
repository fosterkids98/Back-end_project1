from flask import request, jsonify, abort
from . import ticket_bp
from ...models import Ticket, Mechanic, Inventory, ServiceTicketInventory
from ...extensions import db
from .schemas import ticket_schema, tickets_schema
from ...utils.util import token_required, mechanic_required


@ticket_bp.route('/<int:ticket_id>/add-part', methods=['POST'])
@mechanic_required
def add_part_to_ticket(ticket_id, current_mechanic_id=None):
    data = request.get_json()
    part_id = data.get('part_id')
    quantity = data.get('quantity', 1)
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return jsonify({"error": f"Ticket {ticket_id} not found"}), 404

    part = Inventory.query.get(part_id)
    if not part:
        return jsonify({"error": f"Part {part_id} not found"}), 404
    existing = ServiceTicketInventory.query.filter_by(ticket_id=ticket.id, part_id=part.id).first()
    
    if existing:
        existing.quantity += quantity
    else:
        parts_quantity = ServiceTicketInventory(ticket_id=ticket.id, part_id=part.id, quantity=quantity)
        ticket.parts.append(parts_quantity)

    cost_to_add = part.price * quantity
    ticket.total_cost = (ticket.total_cost or 0) + cost_to_add
    db.session.commit()
    return ticket_schema.dump(ticket), 200


@ticket_bp.route('/<int:ticket_id>/edit', methods=['PUT'])
@mechanic_required
def edit_ticket_mechanics(ticket_id, current_mechanic_id=None):
    data = request.get_json()
    remove_ids = data.get('remove_ids', [])
    add_ids = data.get('add_ids', [])

    ticket = Ticket.query.get_or_404(ticket_id)
    # Remove
    ticket.mechanics = [m for m in ticket.mechanics if m.id not in remove_ids]
    # Add
    new_mechs = Mechanic.query.filter(Mechanic.id.in_(add_ids)).all()
    ticket.mechanics.append(new_mechs)

    db.session.commit()
    return ticket_schema.dump(ticket), 200


@ticket_bp.route('/my-tickets', methods=['GET'])
@token_required
def my_tickets(current_user_id=None):
    tickets = Ticket.query.filter_by(customer_id=current_user_id).all()
    return jsonify(tickets_schema.dump(tickets, many=True)), 200

@ticket_bp.route('/', methods=['GET'])
@mechanic_required
def get_tickets(current_mechanic_id=None):
    return jsonify(tickets_schema.dump(Ticket.query.all()))

@ticket_bp.route('/', methods=['POST'])
@mechanic_required
def create_ticket(current_mechanic_id=None):
    new_ticket = ticket_schema.load(request.json, session=db.session)
    db.session.add(new_ticket)
    db.session.commit()
    return ticket_schema.dump(new_ticket), 201

@ticket_bp.route('/<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
@mechanic_required
def assign_mechanic(ticket_id, mechanic_id, current_mechanic_id=None):
    ticket = Ticket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)
    ticket.mechanics.append(mechanic)  # assign directly
    db.session.commit()
    return ticket_schema.dump(ticket)

@ticket_bp.route('/<int:ticket_id>/remove-mechanic', methods=['PUT'])
@mechanic_required
def remove_mechanic(ticket_id, current_mechanic_id=None):
    ticket = Ticket.query.get_or_404(ticket_id)
    ticket.mechanic = None  # remove mechanic assignment
    db.session.commit()
    return ticket_schema.dump(ticket)

@ticket_bp.route('/<int:ticket_id>', methods=['PUT'])
@mechanic_required
def update_ticket(ticket_id, current_mechanic_id=None):
    ticket = Ticket.query.get_or_404(ticket_id)
    updated_ticket = ticket_schema.load(request.json, instance=ticket, partial=True, session=db.session)
    db.session.commit()
    return ticket_schema.dump(updated_ticket)
