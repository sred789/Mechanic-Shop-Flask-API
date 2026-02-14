from marshmallow import fields
from ..extensions import ma
from ..models import ServiceTicket


class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        load_instance = True
        include_fk = True

    mechanic_ids = fields.Method("get_mechanic_ids", dump_only=True)
    part_ids = fields.Method("get_part_ids", dump_only=True)

    def get_mechanic_ids(self, obj):
        return [m.id for m in obj.mechanics]

    def get_part_ids(self, obj):
        return [p.id for p in obj.parts]


service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)