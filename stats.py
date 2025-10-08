from extensions import db
from sqlalchemy import text
from typing import List, Dict

def obtener_stats_completas(carrera: str = "") -> List[Dict]:
    parametros = {}
    where_clause = ""

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
           	ROUND(AVG(promedio_anterior), 2) AS promedio_carrera,
           	ROUND(AVG(peso), 2) AS peso_carrera,
           	ROUND(AVG(altura), 2) AS altura_carrera,
           	ROUND(AVG(edad), 2) AS edad_carrera,
           	SUM(CASE WHEN sexo = 'M' THEN 1 ELSE 0 END) AS total_hombres,
           	SUM(CASE WHEN sexo = 'F' THEN 1 ELSE 0 END) AS total_mujeres,
           	COALESCE(ROUND(
       	        SUM(CASE WHEN sexo = 'M' THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(id_r), 0),
            2), 0) AS porcentaje_hombres,
            COALESCE(ROUND(
                SUM(CASE WHEN sexo = 'F' THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(id_r), 0),
            2), 0) AS porcentaje_mujeres,
            SUM(discapacidad) AS discapacidad_carrera,
            SUM(CASE WHEN discapacidad != 0 AND sexo = 'F' THEN 1 ELSE 0 END) AS discapacidad_mujeres,
            SUM(CASE WHEN discapacidad != 0 AND sexo = 'M' THEN 1 ELSE 0 END) AS discapacidad_hombres,
            COALESCE(ROUND(
                SUM(CASE WHEN discapacidad != 0 AND sexo = 'F' THEN 1 ELSE 0 END) * 100.0 / NULLIF(SUM(discapacidad), 0),
            2), 0) AS porcentaje_discapacidad_mujeres,
            COALESCE(ROUND(
                SUM(CASE WHEN discapacidad != 0 AND sexo = 'M' THEN 1 ELSE 0 END) * 100.0 / NULLIF(SUM(discapacidad), 0),
            2), 0) AS porcentaje_discapacidad_hombres,
            SUM(trabaja) AS trabaja_carrera,
            SUM(CASE WHEN trabaja != 0 AND sexo = 'F' THEN 1 ELSE 0 END) AS trabaja_mujeres,
            SUM(CASE WHEN trabaja != 0 AND sexo = 'M' THEN 1 ELSE 0 END) AS trabaja_hombres,
            COALESCE(ROUND(
                SUM(CASE WHEN trabaja != 0 THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(id_r), 0),
            2), 0) AS porcentaje_trabaja,
            COALESCE(ROUND(
                SUM(CASE WHEN trabaja != 0 AND sexo = 'F' THEN 1 ELSE 0 END) * 100.0 / NULLIF(SUM(trabaja), 0),
            2), 0) AS porcentaje_trabaja_mujeres,
            COALESCE(ROUND(
                SUM(CASE WHEN trabaja != 0 AND sexo = 'M' THEN 1 ELSE 0 END) * 100.0 / NULLIF(SUM(trabaja), 0),
            2), 0) AS porcentaje_trabaja_hombres
        FROM
            respuestas
        {where_clause}
        {groupby_clause}
        ORDER BY
            total_alumnos DESC;
    """)

    stats_generales = db.session.execute(sql_query_general, parametros).all()
    stats_generales_dict = [dict(row._mapping) for row in stats_generales]

    groupby_edades_clause = "GROUP BY edad" if not carrera else "GROUP BY carrera, edad"
    select_edades_carrera = "'Todas' AS carrera" if not carrera else "carrera"

    sql_query_edades = text(f"""
        SELECT
            {select_edades_carrera},
            edad,
            COUNT(edad) AS total_por_edad
        FROM
            respuestas
        {where_clause}
        {groupby_edades_clause}
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
