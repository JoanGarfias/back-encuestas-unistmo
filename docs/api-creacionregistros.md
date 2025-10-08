# 📥 Endpoint de registro: `/crearregistro`

Este endpoint permite registrar a un usuario mediante una solicitud POST que contiene datos personales y académicos en formato JSON. Los datos se validan antes de ser almacenados en la base de datos.

## 🧾 Formato esperado del JSON en el body de la consulta a la API

---

## ✅ Ejemplo

```json
{
  "carrera": "Ing. Computación",
  "nombre": "Juan Pérez",
  "edad": 21,
  "sexo": "M",
  "semestre": 5,
  "promedio_anterior": 8.7,
  "tiempo_traslado": 30,
  "trabaja": 1,
  "gasto_mensual": 1500.50,
  "discapacidad": 0,
  "peso": 70.5,
  "altura": 175,
  "correo": "juan@example.com"
}
````

---

## ✅ Validaciones realizadas

| Campo               | Validación                                                                |
| ------------------- | ------------------------------------------------------------------------- |
| `carrera`           | No puede ser vacío                                                        |
| `nombre`            | No puede ser vacío                                                        |
| `edad`              | Debe ser un número entre 0 y 100                                          |
| `sexo`              | Debe ser `'M'` o `'F'`                                                    |
| `semestre`          | Debe pertenecer a: `[1, 3, 5, 7, 9]` o `[2, 4, 6, 8, 10]`                 |
| `promedio_anterior` | Valor entre 0.0 y 10.0                                                    |
| `altura`            | Entre 100 y 230 cm                                                        |
| `tiempo_traslado`   | Entre 0 y 300 minutos                                                     |
| `trabaja`           | 0 (no) o 1 (sí)                                                           |
| `gasto_mensual`     | Debe ser mayor a 0.0                                                      |
| `discapacidad`      | 0 (no) o 1 (sí)                                                           |
| `peso`              | Entre 40 y 200 kg                                                         |
| `correo`            | No puede ser vacío                                                        |

## 🔁 Respuestas posibles

### 🟢 Éxito

```json
{
  "status": "success",
  "mensaje": "Registro exitoso!"
}
```

**Código HTTP:** `201 Created`

---

### 🔴 Error de validación o de sistema

```json
{
  "status": "error",
  "mensaje": "Descripción del error"
}
```

**Código HTTP:** `400 Bad Request`

Ejemplos de errores posibles:

* `"Carrera no válida."`
* `"Edad no válida."`
* `"Altura no válida."`
* `"Sin datos en el body."`

---