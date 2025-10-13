from extensions import db
from sqlalchemy import text
from typing import List, Dict

import io
import pandas as pd
from pandas import DataFrame
import importlib


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

def generar_reporte_excel(carrera: str = "") -> bytes:
    """Generate an Excel report of the responses, optionally filtered by carrera.
    Returns the Excel file as bytes.
    """

    parametros = {}
    where_clause = ""
    if carrera and carrera != "":
        where_clause = "WHERE carrera = :carrera_param"
        parametros['carrera_param'] = carrera

    sql_query = text(f"""
        SELECT * FROM respuestas
        {where_clause}
    """)

    cursor_result = db.session.execute(
        sql_query,
        parametros
    )

    column_names = cursor_result.keys()
    rows = cursor_result.fetchall()

    # Build DataFrame
    df = DataFrame([dict(zip(column_names, row)) for row in rows])

    # Try to write Excel using available engine. Prefer openpyxl, then xlsxwriter.
    output = io.BytesIO()
    try:
        if importlib.util.find_spec('openpyxl') is not None:
            engine = 'openpyxl'
        elif importlib.util.find_spec('xlsxwriter') is not None:
            engine = 'xlsxwriter'
        else:
            engine = None

        if engine:
            with pd.ExcelWriter(output, engine=engine) as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
            output.seek(0)
            return output.getvalue()
        else:
            # Fallback: return CSV bytes
            csv_bytes = df.to_csv(index=False).encode('utf-8')
            return csv_bytes

    except Exception as e:
        # Re-raise so caller can handle/log
        raise