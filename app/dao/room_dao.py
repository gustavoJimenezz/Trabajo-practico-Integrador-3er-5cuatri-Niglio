from app.extensions import db
from app.models.room import Room
from app.models.booking import Booking
from app.dao.user_dao import UserDAO

class RoomDAO:
    # Crear nueva habitación
    @staticmethod
    def create_room(numero, precio):
        new_room = Room(numero, precio)
        db.session.add(new_room)
        db.session.commit()
        return new_room

    # Obtener habitación por ID
    @staticmethod
    def get_room_by_id(room_id):
        return Room.query.get(room_id)
    
    @staticmethod
    def get_room_by_number(habitacion_num):
        return Room.query.filter(Room._numero == habitacion_num).first()

    
    # Obtener habitación por ID
    @staticmethod
    def get_room_by_id_whit_booking(room_id):
        room = Room.query.get(room_id)

        if not room:
            return None

        reservas_list = []
        for reserva in room.reservas:
            usuario = UserDAO.get_user_by_id(reserva._user_id)
            usuario_str = f"{usuario._email} ({usuario._id})"
            reservas_list.append({
                "id": reserva._id,
                "inicio": reserva._fecha_inicio.isoformat(),
                "fin": reserva._fecha_fin.isoformat(),
                "usuario": usuario_str
            })

        return {
            "id": room._id,
            "numero": room._numero,
            "precio": str(room._precio),
            "reservas": reservas_list
        }


    # Obtener habitación por número
    @staticmethod
    def get_room_by_numero(numero):
        return Room.query.filter_by(_numero=numero).first()
    
    # Obtener habitación filtrado por precio
    @staticmethod
    def get_room_by_price(precio):
        return Room.query.filter(Room._precio <= precio).all()

    # Traer todas las habitaciones
    @staticmethod
    def get_all_rooms():
        return Room.query.all()

    # Editar el precio de una habitación
    @staticmethod
    def update_room_price(room_id, nuevo_precio):
        room = Room.query.get(room_id)
        if room:
            room._precio = nuevo_precio
            db.session.commit()
        return room

    # Cambiar estado (activa/inactiva)
    @staticmethod
    def set_room_status(room_id, activa):
        room = Room.query.get(room_id)
        if room:
            room._activa = activa
            db.session.commit()
        return room
    
        # Buscar habitaciones ocupadas en un rango
    @staticmethod
    def get_occupied_room_ids(fecha_inicio, fecha_fin):
        subq = db.session.query(Booking._room_id).filter(
            Booking._fecha_fin > fecha_inicio,
            Booking._fecha_inicio < fecha_fin
        ).subquery()
        return subq

    # Traer habitaciones activas y disponibles
    @staticmethod
    def get_available_rooms(fecha_inicio, fecha_fin):
        subq = RoomDAO.get_occupied_room_ids(fecha_inicio, fecha_fin)
        return Room.query.filter(
            Room._activa == True,
            ~Room._id.in_(subq)
        ).all()