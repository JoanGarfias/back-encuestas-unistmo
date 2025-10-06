from extensions import db
from sqlalchemy import text
from typing import List, Dict

def obtener_reporte_completo(page: int, num_elements: int, carrera: str) -> List[Dict]:

    offset = page * num_elements
    parametros = {
        "offset": offset,
        "count": num_elements
    }

    where_clause = ""
    if carrera and carrera != "":
        where_clause = "WHERE carrera = :carrera_param"
        parametros['carrera_param'] = carrera

    sql_query = text(f"""
        SELECT * FROM respuestas
        {where_clause}
        LIMIT :offset, :count
    """)

    cursor_result = db.session.execute(
        sql_query,
        parametros
    )

    column_names = cursor_result.keys()
    rows = cursor_result.fetchall()
    lista_json = [dict(zip(column_names, row)) for row in rows]

    return lista_json
