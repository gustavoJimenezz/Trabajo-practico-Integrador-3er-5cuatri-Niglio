from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.dao.room_dao import RoomDAO
from app.dao.booking_dao import BookingDAO
from app.schemas.room_schema import room_schema, rooms_schema, rooms_schema_filter_by_price
from app.utils.validations import error_400, error_403, error_404, error_409, error_500
from app.utils.security import role_required
from datetime import datetime

room_redprint = Blueprint("rooms", __name__)

# 1. Obtener todas las habitaciones
@room_redprint.route("/", methods=["GET"])
@jwt_required()
def get_all_rooms():
    rooms = RoomDAO.get_all_rooms()
    return {"habitaciones" : rooms_schema.dump(rooms)}, 200

# 2. Obtener una habitación por ID
@room_redprint.route("/<int:room_id>", methods=["GET"])
@jwt_required()
def get_room_by_id(room_id):
    room = RoomDAO.get_room_by_id_whit_booking(room_id)
    if not room:
        return error_404("Habitacion no encontrada")
    return room, 200

# 3. Crear nueva habitación (solo empleados)
@room_redprint.route("/", methods=["POST"])
@jwt_required()
@role_required("empleado")
def create_room():

    data = request.get_json()
    numero = data.get("numero")
    precio = data.get("precio")
    activa = data.get("activa", True)

    if not numero or not isinstance(precio, (int, float)):
        return error_400("Numero y precio validos son requeridos")

    if precio <= 0:
        return error_400("El precio debe ser mayor a cero")

    if RoomDAO.get_room_by_numero(numero):
        return error_409("Ya existe una habitacion con ese numero")

    room = RoomDAO.create_room(numero, precio)
    return {"mensaje": "Habitacion creada !"}, 201

# 4. Actualizar precio de una habitación (solo empleados)
@room_redprint.route("/<int:room_id>/precio", methods=["PUT"])
@jwt_required()
@role_required("empleado")
def update_price(room_id):

    data = request.get_json()
    nuevo_precio = data.get("precio")

    if not isinstance(nuevo_precio, (int, float)) or nuevo_precio <= 0:
        return error_400("Precio inválido. Debe ser mayor a cero")

    room = RoomDAO.update_room_price(room_id, nuevo_precio)
    if not room:
        return error_404("Habitación no encontrada")

    return {"mensaje" : "Precio editado! "}, 200

# 5. Cambiar estado activa/inactiva (solo empleados)
@room_redprint.route("/<int:room_id>", methods=["DELETE"])
@jwt_required()
@role_required("empleado")
def change_status_to_deactivated(room_id):

    room = RoomDAO.set_room_status(room_id, False)
    if not room:
        return error_404("Habitación no encontrada")

    return {"mensaje" : f"Habitacion : {room._id}, desactivada"}, 200

# 5. Cambiar estado activa/inactiva (solo empleados)
@room_redprint.route("/<int:room_id>", methods=["PUT", "POST"])
@jwt_required()
@role_required("empleado")
def change_status_to_activate(room_id):

    room = RoomDAO.set_room_status(room_id, True)
    if not room:
        return error_404("Habitación no encontrada")

    return {"mensaje" : f"Habitacion : {room._id}, Activada"}, 200

@room_redprint.route("/filtrar", methods=["GET"])
@jwt_required()
@role_required("cliente")
def filtrar_por_precio():
    precio = request.args.get("precio")
    if not precio:
        return {"error": "Parámetro 'precio' es obligatorio"}, 400

    try:
        precio = float(precio)
    except ValueError:
        return {"error": "Precio inválido"}, 400

    print(f"precio {precio}")
    habitaciones = RoomDAO.get_room_by_price(precio)

    return rooms_schema_filter_by_price.dump(habitaciones), 200 


@room_redprint.route("/diario", methods=["GET"])
@jwt_required()
@role_required("empleado")
def habitaciones_diario():
    fecha_str = request.args.get("fecha")
    if not fecha_str:
        return {"error": "Falta el parámetro fecha"}, 400
    
    try:
        fecha = datetime.strptime(fecha_str, "%d/%m/%Y").date()
    except ValueError:
        return {"error": "Formato de fecha invalido. Use dd/mm/yyyy"}, 400

    # Obtener todas las habitaciones
    habitaciones = RoomDAO.get_all_rooms()

    resultado = []
    for hab in habitaciones:
        estado = "libre"
        # Consultar si hay alguna reserva activa en esa fecha para esta habitación
        reserva_activa = BookingDAO.get_active_booking_for_room_on_date(hab._id, fecha)

        if reserva_activa:
            estado = "ocupada"

        resultado.append({
                "numero": hab._numero,
                "estado": estado
            })
    
    return jsonify({
        "cantidad": len(resultado),
        "habitaciones": resultado
        }), 200


@room_redprint.route("/disponibles", methods=["GET"])
@jwt_required()
@role_required("cliente")
def get_available_rooms():
    from datetime import datetime

    fecha_inicio_str = request.args.get("inicio")
    fecha_fin_str = request.args.get("fin")

    if not fecha_inicio_str or not fecha_fin_str:
        return error_400("Debes proporcionar las fechas 'inicio' y 'fin' en formato DD/MM/YYYY")

    try:
        inicio = datetime.strptime(fecha_inicio_str, "%d/%m/%Y").date()
        fin = datetime.strptime(fecha_fin_str, "%d/%m/%Y").date()
    except ValueError:
        return error_400("Formato de fechas inválido. Usa DD/MM/YYYY")

    disponibles = RoomDAO.get_available_rooms(inicio, fin)

    resultado = [
        {
            "id": hab._id,
            "numero": hab._numero,
            "precio": hab._precio
        }
        for hab in disponibles
    ]

    return resultado, 200
