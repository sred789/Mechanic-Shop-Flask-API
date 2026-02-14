from flask import request, jsonify

from . import service_ticket_bp
from ..extensions import db, cache
from ..models import ServiceTicket, Mechanic, Inventory
from .schemas import service_ticket_schema, service_tickets_schema


# -----------------------------
# CREATE TICKET
# -----------------------------
@service_ticket_bp.route("/", methods=["POST"])
def create_ticket():
    ticket = service_ticket_schema.load(request.get_json() or {})
    db.session.add(ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 201


# -----------------------------
# GET ALL TICKETS (CACHED)
# -----------------------------
@service_ticket_bp.route("/", methods=["GET"])
@cache.cached(timeout=30)
def get_tickets():
    tickets = ServiceTicket.query.all()
    return service_tickets_schema.jsonify(tickets)


# -----------------------------
# ASSIGN MECHANIC
# -----------------------------
@service_ticket_bp.route("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>", methods=["PUT"])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mech = Mechanic.query.get_or_404(mechanic_id)

    if mech not in ticket.mechanics:
        ticket.mechanics.append(mech)
        db.session.commit()

    return service_ticket_schema.jsonify(ticket)


# -----------------------------
# REMOVE MECHANIC
# -----------------------------
@service_ticket_bp.route("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>", methods=["PUT"])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mech = Mechanic.query.get_or_404(mechanic_id)

    if mech in ticket.mechanics:
        ticket.mechanics.remove(mech)
        db.session.commit()

    return service_ticket_schema.jsonify(ticket)


# -----------------------------
# EDIT TICKET
# -----------------------------
@service_ticket_bp.route("/<int:ticket_id>/edit", methods=["PUT"])
def edit_ticket(ticket_id):
    """
    Body example:
    {
      "description": "Brake replacement",
      "vin": "1HGCM82633A004352",
      "status": "closed"
    }
    """

    ticket = ServiceTicket.query.get_or_404(ticket_id)
    data = request.get_json() or {}

    if "description" in data:
        ticket.description = data["description"]

    if "vin" in data:
        ticket.vin = data["vin"]

    if "status" in data:
        ticket.status = data["status"]

    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200


# -----------------------------
# ADD PART TO TICKET
# -----------------------------
@service_ticket_bp.route("/<int:ticket_id>/add-part/<int:part_id>", methods=["PUT"])
def add_part(ticket_id, part_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    part = Inventory.query.get_or_404(part_id)

    if part not in ticket.parts:
        ticket.parts.append(part)
        db.session.commit()

    return service_ticket_schema.jsonify(ticket)