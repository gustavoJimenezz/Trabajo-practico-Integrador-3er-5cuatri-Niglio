from app.extensions import db
from app.models.user import User
import bcrypt

class UserDAO:
    # para crear un nuevo usuario con contraseña hasheada
    @staticmethod
    def create_user(email, password, role):

        new_user = User(
            email=email,
            password=password,
            role=role,
        )

        db.session.add(new_user)
        db.session.commit()
        return new_user
    
    # para buscar un usuario a partir de su email
    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(_email=email).first()

    # para buscar un usuario a partir de su ID
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    # para traer todos los usuarios del sistema
    @staticmethod
    def get_all_users():
        return User.query.all()

    # para modificar el estado activo/inactivo de un usuario.
    @staticmethod
    def change_user_status(user_id, activo):
        user = User.query.get(user_id)
        if user:
            user._activo = activo
            db.session.commit()
        return user

    # para actualizar el rol de un usuario.
    @staticmethod
    def update_user_rol(user_id, new_rol):
        user = User.query.get(user_id)
        if user:
            user._rol = new_rol
            db.session.commit()
        return user

    # para autenticar al usuario comparando el hash almacenado con el password recibido.
    # usa el método check_password() del modelo User.
    @staticmethod
    def authenticate(email, password):
        user = UserDAO.get_user_by_email(email)
        if user and user.check_password(password):
            return user
        return None