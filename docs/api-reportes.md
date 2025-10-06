# 📊 Endpoint de Reportes de Encuesta

Este documento describe el uso del endpoint `/reporte` para obtener los datos brutos de la encuesta con funcionalidad de paginación y filtrado por carrera.

## 1. GET /reporte

Obtiene una página de resultados de la encuesta. Permite paginar y filtrar los registros para su visualización.

### Parámetros de Consulta (Query Parameters)

Todos los parámetros son opcionales.

| **Parámetro** | **Tipo** | **Valor por Defecto** | **Descripción** |
| :--- | :--- | :--- | :--- |
| `page` | `int` | `0` | El índice de la página que se desea obtener (la paginación comienza en la página 0). |
| `num_elements` | `int` | `10` | La cantidad de registros a devolver en una sola página. |
| `id_c` | `int` | **Sin filtro** (`-1`) | **ID numérico de la carrera** por la cual se desea filtrar. |

**Flujo del Filtro por ID (`id_c`):**

1. **Si se omite `id_c` o se envía `id_c=-1`:** El *endpoint* devuelve **TODOS** los registros, ignorando el filtro de carrera.

2. **Si se envía `id_c=3`:** El *endpoint* busca el nombre de la carrera (ej. "Ing. Diseño") y solo devuelve los registros que coincidan con ese nombre.

3. **Si se envía un `id_c` inválido (ej. fuera de rango):** La API devolverá un código de error `400` o `404`.

### Códigos de Carrera Válidos

Para que el filtro funcione, el `id_c` debe coincidir con la lista de carreras definida en el *back-end*:

| **ID** | **Nombre de Carrera** |
| :--- | :--- |
| 1 | Ing. Computación |
| 2 | Ing. Industrial |
| 3 | Ing. Diseño |
| 4 | Ing. Química |
| 5 | Ing. Energía Renovables |
| 6 | Lic. Matemáticas Aplicadas |
| 7 | Ing. Petróleos |

### Ejemplo de Uso

#### A. Paginación Básica

Obtiene la **tercera página** (índice 2) con 20 elementos por página, sin aplicar filtro de carrera.

GET /reporte?page=2&num_elements=20


#### B. Paginación con Filtro

Obtiene la primera página de 10 elementos para la **Ingeniería Química** (`id_c=4`).

GET /reporte?id_c=4&page=0&num_elements=10


### Estructura de la Respuesta (200 OK)

El *endpoint* devuelve un objeto JSON con los resultados paginados, donde cada elemento del array `reporte` corresponde a un registro de la base de datos.

```json
{
    "reporte": [
        {
            "id_r": 1,
            "correo": "",
            "carrera": "Ing. Computación",
            "nombre": "Angel Daniel Jiménez Pacheco",
            "edad": 22,
            "sexo": "M",
            "fecha_registro": "2025-10-01T13:40:23",
            "promedio_anterior": 9.2,
            "tiempo_traslado": 40,
            "trabaja": true,
            "gasto_mensual": 2500.0,
            "discapacidad": false,
            "peso": 51.0,
            "altura": 1.66
        },
        // ... (otros 9-19 registros, dependiendo de num_elements)
    ]
}

```

### Respuestas de error

### Respuestas de Error

| **Código** | **Descripción** | **Causa** |
| :--- | :--- | :--- |
| **400 Bad Request** | `{"error": "El ID de carrera debe ser un número entero válido."}` | El valor pasado a `id_c` o `page`/`num_elements` no pudo convertirse a número (ej: `id_c=abcd`). |
| **404 Not Found** | El filtro se aplica, pero no se encuentran registros. | La página solicitada está fuera del límite o no hay datos para el filtro aplicado. |
| **500 Internal Server Error** | Problemas de conexión a la base de datos o error interno del servidor. |
