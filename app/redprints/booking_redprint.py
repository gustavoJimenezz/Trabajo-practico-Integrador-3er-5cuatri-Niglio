from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.dao.booking_dao import BookingDAO
from app.dao.room_dao import RoomDAO
from app.dao.user_dao import UserDAO
from app.schemas.booking_schema import booking_schema, bookings_schema
from datetime import datetime, timedelta
from app.utils.validations import error_400, error_403, error_404, error_409, error_500

booking_redprint = Blueprint("booking", __name__)

# 1. Ver todas las reservas
@booking_redprint.route("/", methods=["GET"])
@jwt_required()
def get_bookings():
    user_id = get_jwt_identity()
    user = UserDAO.get_user_by_id(user_id)

    if user._role == "empleado":
        bookings = BookingDAO.get_all_bookings()
    else:
        bookings = BookingDAO.get_bookings_by_user(user_id)

    return jsonify(bookings_schema.dump(bookings)), 200

# 2. Ver una reserva específica
@booking_redprint.route("/<int:booking_id>", methods=["GET"])
@jwt_required()
def get_booking(booking_id):
    reserva = BookingDAO.get_booking_by_id(booking_id)
    if not reserva:
        return error_404("Reserva no encontrada")

    user_id = get_jwt_identity()
    user = UserDAO.get_user_by_id(user_id)

    if user._rol != "empleado" and reserva._usuario_id != user_id:
        return error_403("No autorizado para ver esta reserva")

    return jsonify(booking_schema.dump(reserva)), 200

# 3. Crear nueva reserva
@booking_redprint.route("/", methods=["POST"])
@jwt_required()
def create_booking():
    data = request.get_json()
    user_id = get_jwt_identity()

    habitacion_num = data.get("habitacion")
    fecha_inicio = data.get("inicio")
    fecha_fin = data.get("fin")

    if not habitacion_num or not fecha_inicio or not fecha_fin:
        return error_400("Faltan datos obligatorios")

    try:
        inicio = datetime.strptime(fecha_inicio, "%d/%m/%Y").date()
        fin = datetime.strptime(fecha_fin, "%d/%m/%Y").date()
    except ValueError:
        return error_400("Formato de fechas inválido. Usar YYYY-MM-DD")

    if inicio >= fin:
        return error_400("La fecha de inicio debe ser anterior a la de fin")

    habitacion = RoomDAO.get_room_by_number(habitacion_num)
    if not habitacion or not habitacion._activa:
        return error_400("La habitacion no existe o no esta activa")

    # Validar solapamientos + tiempo de limpieza
    reservas_existentes = BookingDAO.get_bookings_by_room(habitacion._id)
    for reserva in reservas_existentes:
        if not (
            fin <= reserva._fecha_inicio or
            inicio >= reserva._fecha_fin
        ):
            return error_409("Ya existe una reserva en ese rango")

    nueva = BookingDAO.create_booking(
        habitacion_id=habitacion._id,
        usuario_id=user_id,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )

    return {"mensaje" : "Reserva creada !"}, 201

# 4. Cancelar reserva (propia o cualquier si es empleado)
@booking_redprint.route("/<int:booking_id>/cancelar", methods=["PATCH"])
@jwt_required()
def cancelar_reserva(booking_id):
    user_id = get_jwt_identity()
    user = UserDAO.get_user_by_id(user_id)

    reserva = BookingDAO.get_booking_by_id(booking_id)
    if not reserva:
        return error_404("Reserva no encontrada")

    if user._rol != "empleado" and reserva._usuario_id != user_id:
        return error_403("No tenés permiso para cancelar esta reserva")

    actualizada = BookingDAO.update_booking_status(booking_id, "cancelada")
    return jsonify(booking_schema.dump(actualizada)), 200

# 5. Cambiar estado (solo empleados)
@booking_redprint.route("/<int:booking_id>/estado", methods=["PATCH"])
@jwt_required()
def cambiar_estado(booking_id):
    user_id = get_jwt_identity()
    user = UserDAO.get_user_by_id(user_id)

    if user._rol != "empleado":
        return error_403("Solo empleados pueden cambiar el estado")

    data = request.get_json()
    nuevo_estado = data.get("estado")
    if nuevo_estado not in ["pendiente", "confirmada", "cancelada"]:
        return error_400("Estado inválido")

    reserva = BookingDAO.update_booking_status(booking_id, nuevo_estado)
    if not reserva:
        return error_404("Reserva no encontrada")

    return jsonify(booking_schema.dump(reserva)), 200
