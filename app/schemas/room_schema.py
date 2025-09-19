from app.extensions import ma
from marshmallow import fields, validate

class RoomSchema(ma.Schema):
    id = fields.Int(attribute="_id", dump_only=True)
    numero = fields.Int(attribute="_numero", required=True)
    precio = fields.Float(
        attribute="_precio",
        required=True,
        validate=validate.Range(min=0)
    )
    activa = fields.Bool(attribute="_activa", dump_only=True)

# Schema para una sola habitación
room_schema = RoomSchema()

# Schema para múltiples habitaciones
rooms_schema = RoomSchema(many=True)

# Schema para múltiples habitaciones
rooms_schema_filter_by_price = RoomSchema(many=True, only=["id", "numero", "precio"])