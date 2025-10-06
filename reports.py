from extensions import db
from sqlalchemy import text
from typing import List, Dict

def obtener_reporte_completo(page: int, num_elements: int) -> List[Dict]:

    offset = page * num_elements

    sql_query = text("""
        SELECT * FROM respuestas
        LIMIT :offset, :count
    """)

    cursor_result = db.session.execute(
        sql_query,
        {"offset": offset, "count": num_elements}
    )

    column_names = cursor_result.keys()

    rows = cursor_result.fetchall()

    lista_json = [dict(zip(column_names, row)) for row in rows]

    return lista_json
