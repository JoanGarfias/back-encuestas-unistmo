from extensions import db
from sqlalchemy import text
from typing import List, Dict
import math
from flask import jsonify

def obtener_desviacion_estandar(carrera: str = "") -> List[Dict]:
    try:
        parametros = {}
        where_clause = ""

        #Obtencion de promedios de los datos a los que se les sacara desviacion para la carrera elegida
        if carrera:
            where_clause = "WHERE carrera = :carrera_param"
            parametros['carrera_param'] = carrera
            select_carrera = "carrera"
            groupby_clause = "GROUP BY carrera"
        else:
            select_carrera = "'Todas' AS carrera"
            groupby_clause = ""

        sql_query_general = text(f"""
            SELECT
                {select_carrera},
                COUNT(id_r) AS total_alumnos,
                ROUND(AVG(edad), 2) AS edad_carrera,
                ROUND(AVG(semestre), 2) AS semestre_carrera,
                ROUND(AVG(promedio_anterior), 2) AS promedio_anterior_carrera,
                ROUND(AVG(tiempo_traslado), 2) AS tiempo_traslado_carrera,
                ROUND(AVG(gasto_mensual), 2) AS gasto_mensual_carrera,
                ROUND(AVG(peso), 2) AS peso_carrera,
                ROUND(AVG(altura), 2) AS altura_carrera
            FROM
                respuestas
            {where_clause}
            {groupby_clause}
            ORDER BY
                total_alumnos DESC;
        """)

        stats_generales = db.session.execute(sql_query_general, parametros).all()
        stats_generales_dict = [dict(row._mapping) for row in stats_generales]

        if not stats_generales_dict:
            return ({"status": "error", "mensaje": "No hay datos disponibles"})

        total_alumnos = stats_generales_dict[0]['total_alumnos']

        if total_alumnos < 2:
            return ({"status": "error", "mensaje": "No se puede sacar la desviación con una muestra de 1 o menos datos"})

        #Diccionario donde se guardaran todas las desviaciones de la carrera elegida
        desviacion = {
            "carrera": stats_generales_dict[0]["carrera"],
            "total_alumnos": total_alumnos
        }

        elementos_desviacion = ["edad", "semestre", "promedio_anterior", "tiempo_traslado", "gasto_mensual", "peso", "altura"]

        for item in elementos_desviacion:
            #Por cada elemento en la lista elementos_desviacion, se obtienen todas las muestras de esa carrera, para sacar su desviacion
            sql_query_general = text(f"""
                SELECT
                    id_r,
                    {item}
                FROM
                    respuestas
                {where_clause}
                ORDER BY
                    id_r DESC;
            """)

            muestras = db.session.execute(sql_query_general, parametros).all()
            muestras_dict = [dict(row._mapping) for row in muestras]

            suma_total = 0
            elem = item + "_carrera"
            media = stats_generales_dict[0][elem]
            alumnos_sin_respuesta = 0

            for item2 in muestras_dict:
                #Obtencion de restas al cadrado y sumandolo al total, para poder sacar la varianza
                valor = item2[item]
                if valor is None:
                    alumnos_sin_respuesta += 1       #Si el promedio no existe, se resta un alumno y no se suma
                else:
                    resta_cuadrado = (valor - media) ** 2
                    suma_total += resta_cuadrado

            varianza = suma_total / (total_alumnos - 1 - alumnos_sin_respuesta)
            desviacion_media = math.sqrt(varianza)

            cad_varianza = item + "_varianza"
            cad_desviacion = item + "_desviacion"
            desviacion[cad_varianza] = round(varianza, 2)
            desviacion[cad_desviacion] = round(desviacion_media, 2)

        return desviacion

    except Exception as e:
        print(f"Error en obtener_desviacion_estandar: {e}")
        return {"status": "error", "mensaje": "Error interno en el servidor", "detalle": str(e)}