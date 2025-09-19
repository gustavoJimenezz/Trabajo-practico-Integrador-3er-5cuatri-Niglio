from app.extensions import db
import bcrypt

class User(db.Model):
    __tablename__ = "usuarios"

    _id = db.Column(db.Integer, primary_key=True)
    _email = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column(db.String(128), nullable=False)
    _role = db.Column(db.String(20), nullable=False)  # 'cliente' o 'empleado'
    _activo = db.Column(db.Boolean, default=True)

    def __init__(self, email, password, role):
        self._email = email
        self._password = self.hash_password(password)
        self._role = role
        self._activo = True

    def hash_password(self, plain_text_password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(plain_text_password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def check_password(self, plain_text_password):
        return bcrypt.checkpw(plain_text_password.encode('utf-8'), self._password.encode('utf-8'))
