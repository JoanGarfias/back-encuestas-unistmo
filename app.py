from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')

def inicio():
    datos = {
        "mensaje": "¡Bienvenido a tu API de Flask!",
        "nombre_usuario": "Lucía",
        "tipo_respuesta": "json"
    }
    return jsonify(datos)