from flask import request, jsonify

from . import inventory_bp
from ..extensions import db
from ..models import Inventory
from .schemas import inventory_schema, inventories_schema


@inventory_bp.route("/", methods=["POST"])
def create_part():
    part = inventory_schema.load(request.get_json() or {})
    db.session.add(part)
    db.session.commit()
    return inventory_schema.jsonify(part), 201


@inventory_bp.route("/", methods=["GET"])
def get_parts():
    parts = Inventory.query.all()
    return inventories_schema.jsonify(parts)


@inventory_bp.route("/<int:id>", methods=["PUT"])
def update_part(id):
    part = Inventory.query.get_or_404(id)
    data = request.get_json() or {}

    if "name" in data:
        part.name = data["name"]
    if "price" in data:
        part.price = float(data["price"])

    db.session.commit()
    return inventory_schema.jsonify(part)


@inventory_bp.route("/<int:id>", methods=["DELETE"])
def delete_part(id):
    part = Inventory.query.get_or_404(id)
    db.session.delete(part)
    db.session.commit()
    return jsonify({"message": "Deleted"}), 200