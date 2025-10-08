from flask import Flask, jsonify, request
from flask_cors import CORS
from urllib.parse import quote_plus
from datetime import date, datetime

from sqlalchemy import text
from flask_mail import Mail, Message
import re

# Obtener las variables de entorno (para bd)
from dotenv import load_dotenv
load_dotenv()
from stats import obtener_stats_completas
from reports import obtener_reporte_completo
from services.MailService import enviar_correo_simple

from extensions import db, mail
from models import Respuesta
import os

app = Flask(__name__)

# MYSQL CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SERVER_NAME'] = os.getenv('SERVER_NAME')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Cors config
origins = [
    "http://localhost:5173",
    "https://encuesta.dxicode.com"
]
CORS(app, resources={r"/*": {"origins": origins}})


# --- Configuración de Flask-Mail
app.config['MAIL_SERVER'] = os.getenv('SMTP_HOST')
app.config['MAIL_PORT'] = os.getenv('SMTP_PORT')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('SMTP_USER')
app.config['MAIL_PASSWORD'] = os.getenv('SMTP_PASS')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
print(f"DEBUG: MAIL_DEFAULT_SENDER is set to: {app.config['MAIL_DEFAULT_SENDER']}")

mail.init_app(app)


carreras = [
    {"id": 1, "name": "Ing. Computación"},
    {"id": 2, "name": "Ing. Industrial"},
    {"id": 3, "name": "Ing. Diseño"},
    {"id": 4, "name": "Ing. Química"},
    {"id": 5, "name": "Ing. Energía Renovables"},
    {"id": 6, "name": "Lic. Matemáticas Aplicadas"},
    {"id": 7, "name": "Ing. Petróleos"},
]

def getCarreraName(id: int):
    if(id == -1):
        return ""
    try:
        return carreras[id - 1]["name"]
    except Exception as e:
        return str(e)

# Validar correo

def validar_correo(email):
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(patron, email):
        return False

    query_correo = text("SELECT correo FROM respuestas WHERE correo = :email")
    result = db.session.execute(query_correo, {"email": email})

     # Retorna True si el correo ya está registrado, False si no
    return result.fetchone() is not None


# API ROUTES


# @app.route('/api/correo', methods=['POST'])
# def notificar_registro():
#     data = request.get_json()
#     correo_destino = data.get('correo', 'destinatario@ejemplo.com')

#     asunto = "¡Registro de Encuesta Exitoso!"
#     cuerpo = f"Hola {correo_destino}, gracias por completar la encuesta de la UNISTMO. Tus datos han sido registrados."

#     exito, mensaje = enviar_correo_simple(correo_destino, asunto, cuerpo)

#     if exito:
#         return jsonify({"status": "success", "mensaje": "Notificación enviada."})
#     else:
#         return jsonify({"status": "error", "mensaje": f"Fallo en el envío: {mensaje}"}), 500



@app.route('/api/carreras', methods=['GET'])

def get_carreras():
    return jsonify({
        "carreras": carreras,
        "length": len(carreras),
        "message": "Lista de carreras obtenida exitosamente"
    })

@app.route('/api/semestres', methods=['GET'])

def get_semestres():
    today = datetime.now().strftime("%d-%m")
    if today > "01-10" and today < "09-02":
        semestres = [1,3,5,7,9]
    else:
        semestres = [2,4,6,8,10]
    return jsonify(semestres)



@app.route('/api/stats', methods=['GET'])

def get_stats():
    id_carrera = request.args.get('id_c')
    try:
        id_carrera = int(id_carrera) if id_carrera else -1
        carrera = getCarreraName(id_carrera)
    except Exception as e:
        return jsonify({"error": "El ID de carrera debe ser un número entero válido."}), 400

    resultados = {
        "stats_carrera": obtener_stats_completas(carrera),
    }
    return jsonify(resultados)


@app.route('/api/reporte', methods=['GET'])

def get_reporte():
    id_carrera = request.args.get('id_c')
    try:
        id_carrera = int(id_carrera) if id_carrera else -1
        carrera = getCarreraName(id_carrera)
    except Exception as e:
        return jsonify({"error": "El ID de carrera debe ser un número entero válido."}), 400

    actual_page = request.args.get('page', default=0, type=int)
    num_elements = request.args.get('num_elements', default=10, type=int)
    resultados = {
        "reporte": obtener_reporte_completo(actual_page, num_elements, carrera),
    }
    return jsonify(resultados)


# Validar contraseña
pinAdmin = os.getenv("PIN_ADMIN")

@app.route('/api/login', methods=['POST'])

def post_login():
    contra = request.json.get('password')
    if not contra:
        return jsonify({"error": "La contraseña es requerida.", "code": 400})
    if len(contra) != 5:
        return jsonify({"error": "La contraseña es incorrecta.", "code": 403})
    if pinAdmin == contra:
        return jsonify({"message": "Contraseña correcta.", "code": 200})
    return jsonify({"error": "La contraseña es incorrecta.", "code": 403})


@app.route('/api/crearregistro', methods=['POST'])
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
        "correo": string
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

        # Validar tiempo_traslado
        if(data["tiempo_traslado"] < 0 or data["tiempo_traslado"] > 300):
            return error("Tiempo de traslado no válido.")

        # Validar si trabaja
        if data['trabaja'] not in [0,1]:
            return error("Opcion de trabajo no válida.")

        # Validar gasto mensual
        if(data['gasto_mensual'] < 0.0):
            return error("Gasto mensual no válido.")

        # Validar si tiene una discapacidad
        if data['discapacidad'] not in [0,1]:
            return error("Opcion de discapacidad no válida.")

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
            registro = Respuesta(
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
            db.session.add(registro)
            db.session.commit()

            correo_destino = data["correo"]
            nombre = data["nombre"]
            carrera = data["carrera"]

            asunto = "¡Registro de Encuesta Exitoso!"
            cuerpo = f"Hola {nombre} de {carrera}, gracias por completar la encuesta de la Universidad del Istmo. Tus datos han sido registrados."

            exito, mensaje = enviar_correo_simple(correo_destino, asunto, cuerpo)

            if exito:
                return jsonify({"status": "success", "mensaje": "Notificación enviada."}), 200
            else:
                return jsonify({"status": "error", "mensaje": f"Fallo en el envío: {mensaje}"}), 500
        except Exception as e:
            db.session.rollback()  # Deshacer cambios si ocurrio un error
            return error(f"Ocurrió un error al guardar en la base de datos: {str(e)}")

    return jsonify({"status": "success", "mensaje": "Registro exitoso!"}), 201
