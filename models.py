from .extensions import db
from datetime import datetime, timezone

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.Integer)
    address = db.Column(db.String(200))
    tickets = db.relationship('Ticket', backref='customer')

service_ticket_mechanics = db.Table('service_ticket_mechanics',
    db.Column('ticket_id', db.Integer, db.ForeignKey('ticket.id'), primary_key=True),
    db.Column('mechanic_id', db.Integer, db.ForeignKey('mechanic.id'), primary_key=True))   

class ServiceTicketInventory(db.Model):
    __tablename__ = 'service_ticket_inventory'

    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    part = db.relationship("Inventory")

class Mechanic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.Integer)
    salary = db.Column(db.Float)
    service_tickets = db.relationship('Ticket', secondary=service_ticket_mechanics, backref='mechanic')

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    service_desc = db.Column(db.String(200))
    VIN = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanic.id'))
    mechanics = db.relationship('Mechanic', secondary=service_ticket_mechanics, backref='tickets')
    status = db.Column(db.String(50), nullable=False, default="Open")   
    parts = db.relationship("ServiceTicketInventory", backref="ticket", cascade="all, delete-orphan")
    total_cost = db.Column(db.Float, default=0.0)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Float, nullable=False)
    tickets = db.relationship('ServiceTicketInventory', backref='inventory', cascade="all, delete-orphan")

