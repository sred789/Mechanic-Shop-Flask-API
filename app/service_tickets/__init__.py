from flask import Blueprint

ticket_bp = Blueprint("service_tickets", __name__)

from . import routes