from flask import Flask
from .extensions import db, ma
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)

    # IMPORT BLUEPRINTS
    from .customers import customer_bp
    from .mechanics import mechanic_bp
    from .service_tickets import ticket_bp

    # REGISTER BLUEPRINTS
    app.register_blueprint(customer_bp, url_prefix="/customers")
    app.register_blueprint(mechanic_bp, url_prefix="/mechanics")
    app.register_blueprint(ticket_bp, url_prefix="/service-tickets")

    with app.app_context():
        db.create_all()

    return app