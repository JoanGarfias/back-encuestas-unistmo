from extensions import db
from sqlalchemy import text

def obtener_stats_por_carrera():
    sql_query = text("""
            SELECT
                carrera,
                COUNT(id_r) AS total_alumnos
            FROM
                respuestas
            GROUP BY
                carrera
            ORDER BY
                total_alumnos DESC;
        """)
    resultados = db.session.execute(sql_query).all()
    return [dict(row._mapping) for row in resultados]
