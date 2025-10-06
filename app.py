from flask import Flask, jsonify, request
from flask_cors import CORS
from urllib.parse import quote_plus
from datetime import date, datetime

# Obtener las variables de entorno (para bd)
import os
from dotenv import load_dotenv
load_dotenv()
from stats import obtener_stats_completas
from reports import obtener_reporte_completo

from extensions import db

app = Flask(__name__)

# MYSQL CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Cors config
def isLocalhost(origin):
    return origin == "localhost"
def getOrigins():
    if isLocalhost(app.config['SERVER_NAME']):
        return "localhost"
    else:
        return "https://encuesta.dxicode.com"
CORS(app, resources={r"/*": {"origins": getOrigins() }})


# API ROUTES

@app.route('/carreras', methods=['GET'])

def get_carreras():
    carreras = [
        "Ing. Computación",
        "Ing. Industrial",
        "Ing. Diseño",
        "Ing. Química",
        "Ing. Energía Renovables",
        "Lic. Matemáticas Aplicadas",
        "Ing. Petróleos",
    ]
    return jsonify({
        "carreras": carreras,
        "length": len(carreras),
        "message": "Lista de carreras obtenida exitosamente"
    })

@app.route('/semestres', methods=['GET'])

def get_semestres():
    today = datetime.now().strftime("%d-%m")
    if today < "01-10":
        semestres = [1,3,5,7,9]
    else:
        semestres = [2,4,6,8,10]
    return jsonify(semestres)



@app.route('/stats', methods=['GET'])

def get_stats():
    carrera = request.args.get('carrera')
    resultados = {
        "stats_carrera": obtener_stats_completas(carrera),
    }
    return jsonify(resultados)


@app.route('/reporte', methods=['GET'])

def get_reporte():
    #carrera = request.args.get('carrera')
    actual_page = request.args.get('page', default=0, type=int)
    num_elements = request.args.get('num_elements', default=10, type=int)
    resultados = {
        "reporte": obtener_reporte_completo(actual_page, num_elements),
    }
    return jsonify(resultados)


@app.route('/login', methods=['POST'])

def post_login():
    datos = {
        "mensaje": "¡Bienvenido a tu API de Flask!",
        "nombre_usuario": "Lucía",
        "tipo_respuesta": "json"
    }
    return jsonify(datos)


@app.route('/crearregistro', methods=['POST'])
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
            respuestas = Respuesta(
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
            db.session.add(respuestas)
            db.session.commit()
        except Exception as e:
            db.session.rollback()  # Deshacer cambios si ocurrio un error
            return error(f"Ocurrió un error al guardar en la base de datos: {str(e)}")

    return jsonify({"status": "success", "mensaje": "Registro exitoso!"}), 201
