from flask import Blueprint, request
from schemas.registro_schema import RegistroSchema
from schemas.usuario_schema import UsuarioSchema
from models.usuarios import Usuario
from database import db

autenticacion = Blueprint('autenticacion', __name__)

# http://127.0.0.1:5000/registro
@autenticacion.route('/registro', methods=['POST'])
def registro():
    schema = RegistroSchema()

    try:
        data = schema.load(request.json)
    except Exception as e:
        return {"error": str(e)}, 400

    nuevo_usuario = Usuario(
        nombre=data['usuario'],
        categoria=data['categoria'],
        clave=data['clave1']
    )

    db.session.add(nuevo_usuario)
    db.session.commit()

    return {"mensaje" : f"Usuario registrado con éxito usuario : {UsuarioSchema().dump(nuevo_usuario)}"}
