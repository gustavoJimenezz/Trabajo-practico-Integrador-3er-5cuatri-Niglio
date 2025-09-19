from app.extensions import ma
from marshmallow import fields, validate

class UserSchema(ma.Schema):
    id = fields.Int(attribute="_id", dump_only=True)
    email = fields.Email(
        attribute="_email",
        required=True,
        validate=validate.Length(max=100)
    )
    rol = fields.Str(
        attribute="_rol",
        required=True,
        validate=validate.OneOf(["cliente", "empleado"])
    )
    activo = fields.Bool(attribute="_activo", dump_only=True)

# Schema único para un usuario
user_schema = UserSchema()

# Schema para lista de usuarios
users_schema = UserSchema(many=True)