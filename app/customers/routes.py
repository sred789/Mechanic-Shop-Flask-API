from flask import request, jsonify
from sqlalchemy.exc import IntegrityError

from . import customer_bp
from ..extensions import db, cache, limiter
from ..models import Customer, ServiceTicket
from .schemas import customer_schema, customers_schema, login_schema
from ..utils.token import encode_token
from ..utils.token_required import token_required


@customer_bp.route("/", methods=["POST"])
def create_customer():
    data = request.get_json() or {}
    customer = customer_schema.load(data)

   
    customer.set_password(data["password"])

    db.session.add(customer)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already exists"}), 409

    return customer_schema.jsonify(customer), 201


@customer_bp.route("/", methods=["GET"])
@cache.cached(timeout=60)  
def get_customers():
    
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    q = Customer.query.order_by(Customer.id.asc()).paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "items": customers_schema.dump(q.items),
        "page": q.page,
        "per_page": q.per_page,
        "total": q.total,
        "pages": q.pages
    })


@customer_bp.route("/<int:id>", methods=["PUT"])
@token_required
def update_customer(customer_id, id):
    if customer_id != id:
        return jsonify({"error": "Forbidden"}), 403

    customer = Customer.query.get_or_404(id)
    data = request.get_json() or {}

    # allow updating name/email/password
    if "name" in data:
        customer.name = data["name"]
    if "email" in data:
        customer.email = data["email"]
    if "password" in data:
        customer.set_password(data["password"])

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already exists"}), 409

    return customer_schema.jsonify(customer), 200


@customer_bp.route("/<int:id>", methods=["DELETE"])
@token_required
def delete_customer(customer_id, id):
    if customer_id != id:
        return jsonify({"error": "Forbidden"}), 403

    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Deleted"}), 200


@customer_bp.route("/login", methods=["POST"])
@limiter.limit("10 per minute") 
def login():
    creds = login_schema.load(request.get_json() or {})
    customer = Customer.query.filter_by(email=creds["email"]).first()
    if not customer or not customer.check_password(creds["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = encode_token(customer.id)
    return jsonify({"token": token})


@customer_bp.route("/my-tickets", methods=["GET"])
@token_required
def my_tickets(customer_id):
    tickets = ServiceTicket.query.filter_by(customer_id=customer_id).all()
    return jsonify([{
        "id": t.id,
        "description": t.description,
        "vin": t.vin,
        "status": t.status,
        "customer_id": t.customer_id,
        "mechanic_ids": [m.id for m in t.mechanics],
        "part_ids": [p.id for p in t.parts],
    } for t in tickets])