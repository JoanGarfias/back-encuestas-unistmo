from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

# Obtener las variables de entorno (para bd)
import os
from dotenv import load_dotenv
load_dotenv()
from stats import obtener_stats_completas

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
    return jsonify(carreras)

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



@app.route('/login', methods=['POST'])

def post_login():
    datos = {
        "mensaje": "¡Bienvenido a tu API de Flask!",
        "nombre_usuario": "Lucía",
        "tipo_respuesta": "json"
    }
    return jsonify(datos)
