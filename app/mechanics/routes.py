from flask import request, jsonify
from sqlalchemy import func

from . import mechanic_bp
from ..extensions import db
from ..models import Mechanic, mechanic_service_ticket
from .schemas import mechanic_schema, mechanics_schema


@mechanic_bp.route("/", methods=["POST"])
def create_mechanic():
    mechanic = mechanic_schema.load(request.get_json() or {})
    db.session.add(mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 201


@mechanic_bp.route("/", methods=["GET"])
def get_mechanics():
    mechanics = Mechanic.query.all()
    return mechanics_schema.jsonify(mechanics)


@mechanic_bp.route("/<int:id>", methods=["PUT"])
def update_mechanic(id):
    mech = Mechanic.query.get_or_404(id)
    data = request.get_json() or {}

    for field in ["name", "email", "phone", "salary"]:
        if field in data:
            setattr(mech, field, data[field])

    db.session.commit()
    return mechanic_schema.jsonify(mech)


@mechanic_bp.route("/<int:id>", methods=["DELETE"])
def delete_mechanic(id):
    mech = Mechanic.query.get_or_404(id)
    db.session.delete(mech)
    db.session.commit()
    return jsonify({"message": "Deleted"}), 200


@mechanic_bp.route("/top", methods=["GET"])
def top_mechanics():
    # returns mechanics ordered by number of tickets worked on (desc)
    rows = (
        db.session.query(
            Mechanic,
            func.count(mechanic_service_ticket.c.service_ticket_id).label("ticket_count")
        )
        .outerjoin(mechanic_service_ticket, Mechanic.id == mechanic_service_ticket.c.mechanic_id)
        .group_by(Mechanic.id)
        .order_by(func.count(mechanic_service_ticket.c.service_ticket_id).desc())
        .all()
    )

    return jsonify([{
        "id": mech.id,
        "name": mech.name,
        "email": mech.email,
        "phone": mech.phone,
        "salary": mech.salary,
        "ticket_count": int(cnt),
    } for mech, cnt in rows])