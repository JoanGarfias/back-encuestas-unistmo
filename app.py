from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)


def isLocalhost(origin):
    return origin == "localhost"

def getOrigins():
    if isLocalhost(app.config['SERVER_NAME']):
        return "localhost"
    else:
        return "https://encuesta.dxicode.com"

CORS(app, resources={r"/*": {"origins": getOrigins() }})

@app.route('/carreras')

def carreras():
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

@app.route('/semestres')

def semestres():
    today = datetime.now().strftime("%d-%m")
    if today < "01-10":
        semestres = [1,3,5,7,9]
    else:
        semestres = [2,4,6,8,10]
    return jsonify(semestres)

@app.route('/login')

def login():
    datos = {
        "mensaje": "¡Bienvenido a tu API de Flask!",
        "nombre_usuario": "Lucía",
        "tipo_respuesta": "json"
    }
    return jsonify(datos)
