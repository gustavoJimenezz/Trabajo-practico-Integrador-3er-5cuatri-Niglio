from app.extensions import db
from app.models.booking import Booking
from datetime import datetime
from app.models.room import Room

class BookingDAO:
    # Crear nueva reserva
    @staticmethod
    def create_booking(habitacion_id, usuario_id, fecha_inicio, fecha_fin):
        new_booking = Booking(
            habitacion_id,
            usuario_id,
            fecha_inicio,
            fecha_fin
        )
        db.session.add(new_booking)
        db.session.commit()
        return new_booking

    # Obtener todas las reservas
    @staticmethod
    def get_all_bookings():
        return Booking.query.all()

    # Buscar reserva por ID
    @staticmethod
    def get_booking_by_id(booking_id):
        return Booking.query.get(booking_id)

    # Buscar reservas por habitación
    @staticmethod
    def get_bookings_by_room(room_id):
        return Booking.query.filter_by(_room_id=room_id).all()

    # Buscar reservas por usuario
    @staticmethod
    def get_bookings_by_user(user_id):
        return Booking.query.filter_by(_usuario_id=user_id).all()

    # Cancelar una reserva
    @staticmethod
    def cancel_booking(booking_id):
        booking = Booking.query.get(booking_id)
        if booking:
            booking._estado = "cancelada"
            db.session.commit()
        return booking

    # Verificar si una habitación está disponible en un rango de fechas
    @staticmethod
    def is_room_available(habitacion_id, fecha_inicio, fecha_fin):
        reservas = Booking.query.filter(
            Booking._room_id == habitacion_id,
            Booking._fecha_fin > fecha_inicio,
            Booking._fecha_inicio < fecha_fin
        ).all()

        return 

    # Obtener reservas vencidas (por ejemplo: pendientes con fecha de inicio pasada)
    @staticmethod
    def get_expired_pending_bookings():

        hoy = datetime.now().date()
        return Booking.query.filter(
            Booking._estado == "pendiente",
            Booking._fecha_inicio < hoy
        ).all()
    
    
    def get_active_booking_for_room_on_date(room_id, date):
        boking = Booking.query.filter(
                Booking._room_id == room_id,
                Booking._fecha_inicio <= date,
                Booking._fecha_fin >= date
            ).first()
        
        return boking