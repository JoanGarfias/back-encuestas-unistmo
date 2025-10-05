from flask import Flask, jsonify, request
import json

app = Flask(__name__)

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
    data = request.get_json()
    
    """ Formato esperado del JSON en el body
    {
	"matricula": int,
	"nombre": string,
	"edad": int,
	"carrera": string,
	"semestre": int,
	"estatura": int,
	"promedio": double,
	"discapacidad": bool,
	"trabaja": bool,
	"gasto": double
    }
    """



    return data