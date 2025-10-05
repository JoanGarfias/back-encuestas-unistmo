from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy # ejecutar pip install flask flask_sqlalchemy pymysql en la consola si no se tiene de antemano el flask_sqlalchemy
from urllib.parse import quote_plus

# Datos de la base
usuario = 'dummy'
ruta = 'localhost'
base = 'dummy'
password = 'nPS@/zo(_2Qm175O'
encoded_password = quote_plus(password)



app = Flask(__name__)

# Configuracion para la conexion de la base
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{usuario}:{encoded_password}@{ruta}/{base}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    carrera = db.Column(db.Integer, nullable=False)
    semestre = db.Column(db.Integer, nullable=False)
    estatura = db.Column(db.Integer, nullable=False)
    promedio = db.Column(db.Float, nullable=False)
    discapacidad = db.Column(db.Boolean, nullable=False)
    trabaja = db.Column(db.Boolean, nullable=False)
    gasto = db.Column(db.Float, nullable=False)
    rol = db.Column(db.Integer, nullable=False)

@app.route('/')

def inicio():
    datos = {
        "mensaje": "¡Bienvenido a tu API de Flask!",
        "nombre_usuario": "Lucía",
        "tipo_respuesta": "json"
    }
    return jsonify(datos)

@app.route('/dummy', methods=['POST'])
def recibirDatos():
    """ Formato esperado del JSON en el body
        {
        "matricula": int,
        "nombre": string,
        "edad": int,
        "carrera": int, opciones disponibles: 1 quimica,2 petroleos,3 diseño,4 computacion,7 industrial,10 matematicas,16 renovables
        "semestre": int, opciones disponibles: 1, 3, 5, 7, 9 o 2, 4, 6, 8, 10 (solo pares o solo impares, no mezclados)
        "estatura": int,
        "promedio": double,
        "discapacidad": bool,
        "trabaja": bool,
        "gasto": double,
        "rol": int opciones disponibles: 0 alumno, 1 maestro
        }
        """

    def error(desc):
        return jsonify({"status": "error", "mensaje": desc}), 400  # Devuelve un error con codigo 400
        
    if request.method == "POST":
        data = request.get_json()

        if not data:
            return error("Sin datos en el body.")

        # Validar carrera
        if data['carrera'] not in [1, 2, 3, 4, 7, 10, 16]:
            return error("Carrera no válida.")

        # Validar semestre
        if data['semestre'] not in [1, 3, 5, 7, 9] and data['semestre'] not in [2, 4, 6, 8, 10]:
            return error("Semestre no válido.")

        # Validar estatura
        if(data['estatura'] < 100 or data['estatura'] > 230):
            return error("Estatura no válida.")

        # Validar promedio
        if(data['promedio'] < 0.0 or data['promedio'] > 10.0):
            return error("Promedio no válido.")

        # Validar rol
        if data['rol'] not in [0,1]:
            return error("Rol no válido.")
        

        try:
        # Crear un usuario
            user = User(
            matricula=data["matricula"],
            nombre=data["nombre"],
            edad=data["edad"],
            carrera=data["carrera"],
            semestre=data["semestre"],
            estatura=data["estatura"],
            promedio=data["promedio"],
            discapacidad=data["discapacidad"],
            trabaja=data["trabaja"],
            gasto=data["gasto"],
            rol=data["rol"]
        )
        except Exception as e:
            return error(f"Ocurrió un error al crear el usuario: {str(e)}")
        
        # Agregar el usuario a la base 
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()  # Deshacer cambios si ocurrio un error
            return error(f"Ocurrió un error al guardar en la base de datos: {str(e)}")

    return jsonify({"status": "success", "mensaje": "Registro exitoso!"}), 201

    
@app.route('/tabla', methods=['GET'])
def inicio3():
    with app.app_context():
        # Inspeccionar la base
        inspector = inspect(db.engine)
        
        # Ver si la tabla 'user' existe
        if 'user' not in inspector.get_table_names():
            db.create_all()  # Crea la tabla si no existe
            return jsonify({"status": "success", "mensaje": "Tabla creada!"}), 201
        else:
            print("Tabla ya existe.")
            return jsonify({"status": "success", "mensaje": "La tabla ya existe!"}), 200