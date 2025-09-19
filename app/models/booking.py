from app.extensions import db
from datetime import datetime

class Booking(db.Model):
    __tablename__ = "reservas"

    _id = db.Column(db.Integer, primary_key=True)
    
    _room_id = db.Column(db.Integer, db.ForeignKey("habitaciones._id"), nullable=False)
    _user_id = db.Column(db.Integer, db.ForeignKey("usuarios._id"), nullable=False)
    
    _fecha_inicio = db.Column(db.Date, nullable=False)
    _fecha_fin = db.Column(db.Date, nullable=False)
    
    _estado = db.Column(db.String(20), default="pendiente")  # pendiente, pagada, vencida, cancelada
    _fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones ORM (acceso a objetos Room y User desde Booking)
    room = db.relationship("Room", backref="reservas")
    user = db.relationship("User", backref="reservas")

    def __init__(self, room_id, user_id, fecha_inicio, fecha_fin):
        self._room_id = room_id
        self._user_id = user_id
        self._fecha_inicio = fecha_inicio
        self._fecha_fin = fecha_fin
        self._estado = "pendiente"