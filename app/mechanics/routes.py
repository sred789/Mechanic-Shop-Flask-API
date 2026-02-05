from flask import request
from . import mechanic_bp
from app.extensions import db
from app.models import Mechanic
from .schemas import mechanic_schema, mechanics_schema

@mechanic_bp.route("/", methods=["POST"])
def create_mechanic():
    mechanic = mechanic_schema.load(request.json)
    db.session.add(mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 201


@mechanic_bp.route("/", methods=["GET"])
def get_mechanics():
    mechanics = Mechanic.query.all()
    return mechanics_schema.jsonify(mechanics)


@mechanic_bp.route("/<int:id>", methods=["PUT"])
def update_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)

    if not request.is_json:
        return {"error": "Request must be JSON"}, 415

    data = request.get_json()

    for key, value in data.items():
        setattr(mechanic, key, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic)


@mechanic_bp.route("/<int:id>", methods=["DELETE"])
def delete_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    db.session.delete(mechanic)
    db.session.commit()
    return {"message": "Mechanic deleted"}