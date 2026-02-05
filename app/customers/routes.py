from flask import request
from . import customer_bp
from app.extensions import db
from app.models import Customer
from .schemas import customer_schema, customers_schema


# CREATE CUSTOMER
@customer_bp.route("/", methods=["POST"])
def create_customer():
    customer = customer_schema.load(request.json)
    db.session.add(customer)
    db.session.commit()
    return customer_schema.jsonify(customer), 201


# GET ALL CUSTOMERS
@customer_bp.route("/", methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    return customers_schema.jsonify(customers)


# GET ONE CUSTOMER
@customer_bp.route("/<int:id>", methods=["GET"])
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return customer_schema.jsonify(customer)


# UPDATE CUSTOMER
@customer_bp.route("/<int:id>", methods=["PUT"])
def update_customer(id):
    customer = Customer.query.get_or_404(id)

    data = request.get_json(silent=True)
    if not data:
        return {"error": "No JSON body received"}, 400

    for key, value in data.items():
        setattr(customer, key, value)

    db.session.commit()
    return customer_schema.jsonify(customer)


# DELETE CUSTOMER
@customer_bp.route("/<int:id>", methods=["DELETE"])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return {"message": "Customer deleted"}