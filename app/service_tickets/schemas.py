from datetime import datetime

from marshmallow import EXCLUDE, pre_load

from app.extensions import ma
from app.models import ServiceTicket


class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        load_instance = True
        include_relationships = True
        include_fk = True
        unknown = EXCLUDE

    @pre_load
    def normalize_input(self, data, **kwargs):
        # Accept "description" as an alias for the model's service_desc field.
        if "description" in data and "service_desc" not in data:
            data["service_desc"] = data.pop("description")

        # Allow common date formats for service_date (e.g., "02/04/2026").
        service_date = data.get("service_date")
        if isinstance(service_date, str) and "/" in service_date:
            for fmt in ("%m/%d/%Y", "%m/%d/%y"):
                try:
                    data["service_date"] = datetime.strptime(service_date, fmt).date()
                    break
                except ValueError:
                    continue

        return data


ticket_schema = ServiceTicketSchema()
tickets_schema = ServiceTicketSchema(many=True)
