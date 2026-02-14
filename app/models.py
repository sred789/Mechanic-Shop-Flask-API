from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db

# -----------------------------
# Junction Tables (M2M)
# -----------------------------

mechanic_service_ticket = db.Table(
    "mechanic_service_ticket",
    db.Column("mechanic_id", db.Integer, db.ForeignKey("mechanic.id"), primary_key=True),
    db.Column("service_ticket_id", db.Integer, db.ForeignKey("service_ticket.id"), primary_key=True),
)

service_ticket_inventory = db.Table(
    "service_ticket_inventory",
    db.Column("service_ticket_id", db.Integer, db.ForeignKey("service_ticket.id"), primary_key=True),
    db.Column("inventory_id", db.Integer, db.ForeignKey("inventory.id"), primary_key=True),
)

# -----------------------------
# Models
# -----------------------------

class Customer(db.Model):
    __tablename__ = "customer"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    service_tickets = db.relationship("ServiceTicket", back_populates="customer", cascade="all, delete-orphan")

    def set_password(self, raw_password: str) -> None:
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password, raw_password)


class Mechanic(db.Model):
    __tablename__ = "mechanic"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    email = db.Column(db.String(160), unique=True, nullable=True, index=True)
    phone = db.Column(db.String(50), nullable=True)
    salary = db.Column(db.Float, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    service_tickets = db.relationship(
        "ServiceTicket",
        secondary=mechanic_service_ticket,
        back_populates="mechanics",
    )


class Inventory(db.Model):
    __tablename__ = "inventory"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)
    price = db.Column(db.Float, nullable=False)

    service_tickets = db.relationship(
        "ServiceTicket",
        secondary=service_ticket_inventory,
        back_populates="parts",
    )


class ServiceTicket(db.Model):
    __tablename__ = "service_ticket"

    id = db.Column(db.Integer, primary_key=True)

    description = db.Column(db.String(500), nullable=False)
    vin = db.Column(db.String(32), nullable=False)  # <-- NEW
    status = db.Column(db.String(50), default="open")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    customer = db.relationship("Customer", back_populates="service_tickets")

    mechanics = db.relationship(
        "Mechanic",
        secondary=mechanic_service_ticket,
        back_populates="service_tickets",
    )

    parts = db.relationship(
        "Inventory",
        secondary=service_ticket_inventory,
        back_populates="service_tickets",
    )