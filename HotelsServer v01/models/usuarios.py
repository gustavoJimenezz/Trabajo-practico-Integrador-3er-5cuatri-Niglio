from database import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    clave = db.Column(db.String(100), unique=True, nullable=False)
    
    def __init__(self, nombre, categoria, clave):
        self.nombre = nombre
        self.categoria = categoria
        self.clave = clave
    
    def __str__(self):
        return f"id={self.id}, nombre={self.nombre}"
