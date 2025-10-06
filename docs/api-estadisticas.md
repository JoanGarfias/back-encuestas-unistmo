# 📈 Endpoint de Estadísticas (Analytics)

Este documento describe el uso del endpoint `/stats` para obtener métricas agregadas y distribuciones de edad de la encuesta.

## 1. GET /stats

Obtiene un reporte consolidado con estadísticas descriptivas (promedios, conteos, porcentajes) y la distribución de edades.

### Parámetros de Consulta (Query Parameters)

Solo un parámetro de filtro es aceptado:

| **Parámetro** | **Tipo** | **Valor por Defecto** | **Descripción** |
| :--- | :--- | :--- | :--- |
| `id_c` | `int` | **Sin filtro** (`-1`) | **ID numérico de la carrera** por la cual se desea filtrar. |

**Lógica de Agregación (CRUCIAL):**

Este *endpoint* tiene un comportamiento dinámico:

1.  **Modo Universal (Sin Filtro):** Si `id_c` no se envía o es `-1`, el *backend* consolida todas las respuestas de la universidad en una **única fila** de resultados. La columna `carrera` tendrá el valor `'Todas'`.
2.  **Modo Filtrado:** Si `id_c` es válido, el *backend* devuelve una única fila con las estadísticas **solo para esa carrera**.

---

### Estructura de la Respuesta (200 OK)

La respuesta es un objeto JSON que contiene la clave `stats_carrera`, cuyo valor es un **array de un solo elemento** que contiene todas las métricas.

```json
{
    "stats_carrera": [
        {
            "carrera": "Ing. Computación" | "Todas",
            "total_alumnos": 63,

            /* --- Métricas Descriptivas --- */
            "promedio_carrera": 8.34,
            "peso_carrera": 69.72,
            "altura_carrera": 1.68,
            "edad_carrera": 19.67,

            /* --- Distribución de Género --- */
            "total_hombres": 45,
            "total_mujeres": 18,
            "porcentaje_hombres": 71.43,
            "porcentaje_mujeres": 28.57,

            /* --- Distribución de Edad (Anidada) --- */
            "edades": {
                "18": 14,    // Clave: Edad, Valor: Conteo
                "19": 10,
                "20": 15,
                "21": 14,
                "22": 5,
                // ... (El objeto JSON se expande para todas las edades encontradas)
            }
        }
    ]
}

```

### Ejemplos de Uso
1. Obtener Estadísticas de Toda la Universidad (Modo Universal)
GET /stats

2. Obtener Estadísticas de la Carrera de Ingeniería en Computación
GET /stats?id_c=1


### Respuestas de Error

| **Código** | **Descripción** | **Causa** |
| :--- | :--- | :--- |
| **400 Bad Request** | `{"error": "El ID de carrera debe ser un número entero válido."}` | El valor pasado a `id_c` o `page`/`num_elements` no pudo convertirse a número (ej: `id_c=abcd`). |
| **404 Not Found** | El filtro se aplica, pero no se encuentran registros. | La página solicitada está fuera del límite o no hay datos para el filtro aplicado. |
| **500 Internal Server Error** | Problemas de conexión a la base de datos o error interno del servidor. |
