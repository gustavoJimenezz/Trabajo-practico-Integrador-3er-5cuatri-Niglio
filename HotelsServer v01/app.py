from flask import Flask
from database import db
from routes.autenticacion import autenticacion 

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///TP-programacion-hotels.sql"


# Registrar blueprints con las rutas modulares
app.register_blueprint(autenticacion)
db.init_app(app)


# https://flask.palletsprojects.com/en/latest/appcontext/
with app.app_context():
    try:
        db.drop_all()
        db.create_all()
        print("Base de datos creada con exito.")
    except Exception as e:
        print(f"Error al crear una base de datos : {e}")

if __name__ == "__main__":
    app.run(debug=True)
