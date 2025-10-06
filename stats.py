from extensions import db
from sqlalchemy import text

def obtener_stats_completas(carrera = ""):
    parametros = {}
    where_clause = ""

    if carrera:
        where_clause = "WHERE carrera = :carrera_param"
        parametros['carrera_param'] = carrera

    sql_query_general = text(f"""
        SELECT
            carrera,
            COUNT(id_r) AS total_alumnos,
            ROUND(AVG(promedio_anterior), 2) AS promedio_carrera,
            ROUND(AVG(peso), 2) AS peso_carrera,
            ROUND(AVG(altura), 2) AS altura_carrera,
            ROUND(AVG(edad), 2) AS edad_carrera
        FROM
            respuestas
        {where_clause} -- Inyección segura del filtro
        GROUP BY
            carrera
        ORDER BY
            total_alumnos DESC;
    """)

    stats_generales = db.session.execute(sql_query_general, parametros).all()
    stats_generales_dict = [dict(row._mapping) for row in stats_generales]

    sql_query_edades = text(f"""
        SELECT
            carrera,
            edad,
            COUNT(edad) AS total_por_edad
        FROM
            respuestas
        {where_clause} -- Reutilizamos el filtro si existe
        GROUP BY
            carrera, edad
        ORDER BY
            carrera, edad;
    """)

    conteo_edades_result = db.session.execute(sql_query_edades, parametros).all()
    conteo_edades_dict = [dict(row._mapping) for row in conteo_edades_result]

    mapa_edades = {}
    for item in conteo_edades_dict:
        carrera_nombre = item['carrera']
        edad_str = str(item['edad'])
        conteo = item['total_por_edad']

        if carrera_nombre not in mapa_edades:
            mapa_edades[carrera_nombre] = {}

        mapa_edades[carrera_nombre][edad_str] = conteo

    stats_anidadas = []
    for stats in stats_generales_dict:
        carrera_nombre = stats['carrera']
        stats['edades'] = mapa_edades.get(carrera_nombre, {})
        stats_anidadas.append(stats)

    return stats_anidadas
