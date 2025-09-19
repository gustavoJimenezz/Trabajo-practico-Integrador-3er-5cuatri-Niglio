from marshmallow import Schema, fields, validates_schema, ValidationError

class RegistroUsuarioSchema(Schema):
    usuario = fields.Str(required=True)
    categoria = fields.Str(required=True)
    clave1 = fields.Str(required=True)
    clave2 = fields.Str(required=True)

    @validates_schema
    def validar_claves(self, data, **kwargs):
        if data.get('clave1') != data.get('clave2'):
            raise ValidationError('Las claves no coinciden.', field_names=['clave2'])