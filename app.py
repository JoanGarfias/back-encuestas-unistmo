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
        return jsonify({"status": "error", "mensaje": desc}), 400  # Returning a JSON response with a 400 status code.
        
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
            return error("Promedio no válida.")

        # Validar rol
        if data['rol'] not in [0,1]:
            return error("Rol no válido.")
        

        """user = User(
            matricula = data["matricula"],
            nombre = data["nombre"],
            edad = data["edad"],
            carrera = data["carrera"],
            estatura = data["estatura"],
            promedio = data["promedio"],
            discapacidad = data["discapacidad"],
            trabaja = data["trabaja"],
            gasto = data["gasto"],
            rol = data["rol"],
        )"""
        #db.session.add(user)
        #db.session.commit()

    return jsonify({"status": "success", "mensaje": "Registro exitoso!"}), 201

    
