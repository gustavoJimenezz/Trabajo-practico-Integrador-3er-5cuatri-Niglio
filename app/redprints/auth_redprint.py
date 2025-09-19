from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.dao.user_dao import UserDAO
from app.schemas.user_schema import user_schema
from app.schemas.auth_schema_register import RegistroUsuarioSchema
from datetime import timedelta
from app.utils.validations import error_400, error_401, error_409
from flask import request, jsonify
from marshmallow import ValidationError


# Nombre del blueprint, el del archivo
auth_redprint = Blueprint("auth", __name__)

# Endpoint de registro de usuario
@auth_redprint.route("/registro", methods=["POST"])
def register():
    registro_schema = RegistroUsuarioSchema()
    data = request.get_json()
    if not data:
        return error_400("Datos de registro no proporcionados")

    try:
        validated_data = registro_schema.load(data)
    except ValidationError as err:
        return error_400(err.messages)

    email = validated_data["usuario"]
    role = validated_data["categoria"]
    clave = validated_data["clave1"]

    if UserDAO.get_user_by_email(email):
        return error_409("El usuario ya existe")

    new_user = UserDAO.create_user(email=email, password=clave, role=role)
    return jsonify({
        "mensaje": "Usuario creado correctamente",
    }), 201

# Endpoint de login
@auth_redprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return error_400("Datos de login no proporcionados")

    email = data.get("usuario")
    password = data.get("clave")

    if not email or not password:
        return error_400("Los campos son obligatorios")   

    # Verifica credenciales
    user = UserDAO.authenticate(email=email, password=password)
    if not user:
        return error_401("Credenciales invalidas")

    # Crear token JWT
    token = create_access_token(
        identity=str(user._id),
        additional_claims={"rol": user._role},
        expires_delta=timedelta(hours=3)
    )


    return jsonify({
        "token": token,
        "categoria": user._role,
    }), 200