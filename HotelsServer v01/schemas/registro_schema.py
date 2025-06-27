from marshmallow import Schema, fields, validate

class RegistroSchema(Schema):
    id = fields.Int(dump_only=True)
    usuario = fields.Str()
    categoria = fields.Str()
    clave1 = fields.Str()
    clave2 = fields.Str()