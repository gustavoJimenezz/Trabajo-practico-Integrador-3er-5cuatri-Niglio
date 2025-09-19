from app.extensions import ma
from marshmallow import fields

class BookingSchema(ma.Schema):
    id = fields.Int(attribute="_id", dump_only=True)
    room_id = fields.Int(attribute="_room_id", required=True)
    user_id = fields.Int(attribute="_user_id", required=True)
    fecha_inicio = fields.Date(attribute="_fecha_inicio", required=True)
    fecha_fin = fields.Date(attribute="_fecha_fin", required=True)
    estado = fields.Str(attribute="_estado", dump_only=True)

# Schema único
booking_schema = BookingSchema()

# Schema para listas
bookings_schema = BookingSchema(many=True)

class BookingSchema(ma.Schema):
    id = fields.Integer(attribute="_id")
    inicio = fields.Date(attribute="_fecha_inicio")
    fin = fields.Date(attribute="_fecha_fin")
    estado = fields.String(attribute="_estado")

    # Campos anidados o calculados:
    numero = fields.Method("get_habitacion_numero")
    usuario = fields.Method("get_usuario")

    def get_habitacion_numero(self, obj):
        if obj.room:
            return obj.room._numero
        return None

    def get_usuario(self, obj):
        if obj.user:
            return f"{obj.user._email} ({obj.user._id})"
        return None


# Instancias del schema
booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True, only=["id", "numero", "inicio", "fin"])
