from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
# from redis import Redis (descartado desde la aclaracion del profe en la clase del 28/6. No lo usaré)

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
# redis_client = None  # Se inicializa en create_app() pero descartado tb.
