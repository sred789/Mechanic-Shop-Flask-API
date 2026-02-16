from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import create_app
from app.models import Base, Customer, Mechanic, ServiceTicket
from config import DATABASE_URL
import flask.logging as logging

app = create_app('ProductionConfig')

# logging.basicConfig(level=logging.INFO)
# app.logger.setLevel(logging.DEBUG)
# app.logger.info("Starting Flask application with SQLAlchemy")

# Database Engine
engine = create_engine(DATABASE_URL, echo=True)

# Create tables
Base.metadata.create_all(engine)

# Session Factory
Session = sessionmaker(bind=engine)

@app.route("/")
def home():
    return {"message": "Flask + SQLAlchemy is running!"}

# @app.route("/customers")
# def get_customers():
#     session = Session()
#     customers = session.query(Customer).all()

#     data = [
#         {"id": c.id, "name": c.name, "email": c.email, "phone": c.phone}
#         for c in customers
#     ]

#     session.close()
#     return jsonify(data)

# if __name__ == "__main__":
#     app.run(debug=True)