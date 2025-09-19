import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from app.extensions import db, ma, jwt

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_HEADER_NAME"] = "N-Auth"
    app.config["JWT_HEADER_TYPE"] = "bearer"
    
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    from app.redprints.auth_redprint import auth_redprint
    from app.redprints.user_redprint import user_redprint
    from app.redprints.room_redprint import room_redprint
    from app.redprints.booking_redprint import booking_redprint

    app.register_blueprint(auth_redprint)
    app.register_blueprint(user_redprint)
    app.register_blueprint(room_redprint, url_prefix="/habitaciones")
    app.register_blueprint(booking_redprint, url_prefix="/reservas")

    @app.route('/init-db', methods=['GET'])
    def init_db_route():
        try:
            db.create_all()
            return jsonify({"message": "Base de datos creada correctamente"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app
