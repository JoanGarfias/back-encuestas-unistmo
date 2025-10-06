from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy # ejecutar pip install flask flask_sqlalchemy pymysql en la consola si no se tiene de antemano el flask_sqlalchemy
from urllib.parse import quote_plus
from datetime import date

# Datos de la base (rellenar con datos correctos si se van a hacer pruebas)
usuario = 'panela'
ruta = 'localhost'
base = 'queso'
password = 'F6g]x4WcP[oagFxD'
encoded_password = quote_plus(password)



app = Flask(__name__)

# Configuracion para la conexion de la base
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{usuario}:{encoded_password}@{ruta}/{base}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Encuestas(db.Model):
    id_u = db.Column(db.Integer, primary_key=True)
    carrera = db.Column(db.String(128), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    sexo = db.Column(db.Enum("M", "F"), nullable=False)
    semestre = db.Column(db.Integer, nullable=False)
    fecha_registro = db.Column(db.Date, nullable=False)
    promedio_anterior = db.Column(db.Float, nullable=False)
    tiempo_traslado = db.Column(db.Integer, nullable=False)
    trabaja = db.Column(db.Integer, nullable=False)
    gasto_mensual = db.Column(db.Float, nullable=False)
    discapacidad = db.Column(db.Integer, nullable=False)
    peso = db.Column(db.Float, nullable=False)
    altura = db.Column(db.Integer, nullable=False)
    correo = db.Column(db.String(128), nullable=False, unique=True)

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
        "carrera": string,
        "nombre": string,
        "edad": int,
        "sexo": 'M', 'F'
        "semestre": int, opciones disponibles: 1, 3, 5, 7, 9 o 2, 4, 6, 8, 10 (solo pares o solo impares, no mezclados)
        "promedio_anterior": double,
        "tiempo_traslado": int,
        "trabaja": int,
        "gasto_mensual": double,
        "discapacidad": int,
        "peso": double,
        "altura": int,
        "correo", string
        }
        """

    def error(desc):
        return jsonify({"status": "error", "mensaje": desc}), 400  # Devuelve un error con codigo 400
        
    if request.method == "POST":
        data = request.get_json()

        if not data:
            return error("Sin datos en el body.")

        # Validar carrera
        if not data['carrera']:
            return error("Carrera no válida.")

        #Validar nombre
        if not data['nombre']:
            return error("Nombre no válido.")

        # Validar edad
        if(data["edad"] < 0 or data["edad"] > 100):
            return error("Edad no válida.")

        # Validar sexo
        if data['sexo'] not in ["M", "F"]:
            return error("Sexo no válido.")

        # Validar semestre
        if data['semestre'] not in [1, 3, 5, 7, 9] and data['semestre'] not in [2, 4, 6, 8, 10]:
            return error("Semestre no válido.")

        # Validar promedio anterior
        if(data["promedio_anterior"] < 0.0 or data["promedio_anterior"] > 10.0):
            return error("Promedio no válido.")

        # Validar altura
        if(data['altura'] < 100 or data['altura'] > 230):
            return error("Altura no válida.")

        # Validar tiempo_traslado
        if(data["tiempo_traslado"] < 0 or data["tiempo_traslado"] > 300):
            return error("Tiempo de traslado no válido.")

        # Validar si trabaja
        if data['trabaja'] not in [0,1]:
            return error("Opcion de trabajo no válida.")

        # Validar peso
        if(data['peso'] < 40 or data['peso'] > 200):
            return error("Peso no válido.")

        # Validar altura
        if(data['altura'] < 100 or data['altura'] > 230):
            return error("Altura no válida.")

        #Validar correo
        if(not data["correo"]):
            return error("No se permite un correo vacio.")

        try:
        # Crear un usuario
            encuestas = Encuestas(
            carrera=data["carrera"],
            nombre=data["nombre"],
            edad=data["edad"],
            sexo=data["sexo"],
            semestre=data["semestre"],
            fecha_registro=date.today(),
            promedio_anterior=data["promedio_anterior"],
            tiempo_traslado=data["tiempo_traslado"],
            trabaja=data["trabaja"],
            gasto_mensual=data["gasto_mensual"],
            discapacidad=data["discapacidad"],
            peso=data["peso"],
            altura=data["altura"],
            correo=data["correo"]
        )
        except Exception as e:
            return error(f"Ocurrió un error al crear el usuario: {str(e)}")
        
        # Agregar el usuario a la base 
        try:
            db.session.add(encuestas)
            db.session.commit()
        except Exception as e:
            db.session.rollback()  # Deshacer cambios si ocurrio un error
            return error(f"Ocurrió un error al guardar en la base de datos: {str(e)}")

    return jsonify({"status": "success", "mensaje": "Registro exitoso!"}), 201

    
@app.route('/tabla', methods=['GET'])
def inicio3():
    with app.app_context():
        # Inspeccionar la base
        #inspector = inspect(db.engine)
        
        # Ver si la tabla 'encuestas' existe
        #if 'encuestas' not in inspector.get_table_names():
        db.create_all()  # Crea la tabla si no existe
        return jsonify({"status": "success", "mensaje": "Tabla creada!"}), 201
        #else:
        #    print("Tabla ya existe.")
        #    return jsonify({"status": "success", "mensaje": "La tabla ya existe!"}), 200