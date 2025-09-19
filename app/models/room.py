from app.extensions import db

class Room(db.Model):
    __tablename__ = "habitaciones"

    _id = db.Column(db.Integer, primary_key=True)
    _numero = db.Column(db.Integer, unique=True, nullable=False)
    _precio = db.Column(db.Float, nullable=False)
    _activa = db.Column(db.Boolean, default=True)

    def __init__(self, numero, precio):
        self._numero = numero
        self._precio = precio
        self._activa = True
        