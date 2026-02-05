from flask import request
from . import ticket_bp
from app.extensions import db
from app.models import ServiceTicket, Mechanic
from .schemas import ticket_schema, tickets_schema


@ticket_bp.route("/", methods=["POST"])
def create_ticket():
    ticket = ticket_schema.load(request.json)
    db.session.add(ticket)
    db.session.commit()
    return ticket_schema.jsonify(ticket), 201


@ticket_bp.route("/", methods=["GET"])
def get_tickets():
    tickets = ServiceTicket.query.all()
    return tickets_schema.jsonify(tickets)


@ticket_bp.route("/<int:ticket_id>", methods=["PUT"])
def update_ticket(ticket_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    updated = ticket_schema.load(request.json, instance=ticket, partial=True)
    db.session.add(updated)
    db.session.commit()
    return ticket_schema.jsonify(updated)


@ticket_bp.route("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>", methods=["PUT"])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)

    ticket.mechanics.append(mechanic)
    db.session.commit()

    return ticket_schema.jsonify(ticket)


@ticket_bp.route("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>", methods=["PUT"])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)

    ticket.mechanics.remove(mechanic)
    db.session.commit()

    return ticket_schema.jsonify(ticket)
