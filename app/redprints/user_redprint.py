from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.dao.user_dao import UserDAO
from app.schemas.user_schema import user_schema, users_schema
from app.utils.validations import error_400, error_403, error_404, error_409, error_500

user_redprint = Blueprint("users", __name__)

# Obtener todos los usuarios (solo empleados)
@user_redprint.route("/", methods=["GET"])
@jwt_required()
def get_all_users():
    user_id = get_jwt_identity()
    user = UserDAO.get_user_by_id(user_id)

    if user._rol != "empleado":
        return error_403("Acceso restringido a empleados")

    users = UserDAO.get_all_users()
    return jsonify(users_schema.dump(users)), 200

# Obtener usuario por ID
@user_redprint.route("/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user_by_id(user_id):
    actual = UserDAO.get_user_by_id(get_jwt_identity())
    if actual._rol != "empleado":
        return error_403("Acceso restringido a empleados")

    user = UserDAO.get_user_by_id(user_id)
    if not user:
        return error_404("Usuario no encontrado")

    return jsonify(user_schema.dump(user)), 200

# Cambiar estado activo/inactivo
@user_redprint.route("/<int:user_id>/status", methods=["PATCH"])
@jwt_required()
def change_status(user_id):
    actual = UserDAO.get_user_by_id(get_jwt_identity())
    if actual._rol != "empleado":
        return error_403("Acceso restringido a empleados")

    data = request.get_json()
    activo = data.get("activo")

    if not isinstance(activo, bool):
        return error_400("Campo 'activo' debe ser booleano")

    user = UserDAO.change_user_status(user_id, activo)
    if not user:
        return error_404("Usuario no encontrado")

    return jsonify(user_schema.dump(user)), 200

# Cambiar rol del usuario
@user_redprint.route("/<int:user_id>/rol", methods=["PATCH"])
@jwt_required()
def update_rol(user_id):
    actual = UserDAO.get_user_by_id(get_jwt_identity())
    if actual._rol != "empleado":
        return error_403("Acceso restringido a empleados")

    data = request.get_json()
    nuevo_rol = data.get("rol")

    if nuevo_rol not in ["cliente", "empleado"]:
        return error_400("Rol inválido")

    user = UserDAO.update_user_rol(user_id, nuevo_rol)
    if not user:
        return error_404("Usuario no encontrado")

    return jsonify(user_schema.dump(user)), 200