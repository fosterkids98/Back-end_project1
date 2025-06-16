from flask import Blueprint

ticket_bp = Blueprint('service_ticket', __name__, url_prefix='/service_tickets')
from . import routes
