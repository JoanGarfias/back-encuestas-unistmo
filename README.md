# Back-end Encuestas UNISTMO

<img width="1922" height="916" alt="image" src="https://github.com/user-attachments/assets/aef7dd54-9a9d-4e21-a97c-84e9bac952c4" />
<img width="1922" height="916" alt="image" src="https://github.com/user-attachments/assets/398bb7b2-a554-42c0-8c7c-147be81f4d60" />

Este es el repositorio del back-end para el proyecto de encuestas de la materia de Probabilidad y Estadística de la Universidad del Istmo, carrera de Ingeniería en Computación.

## Descripción

El proyecto tuvo como objetivo crear una plataforma para responder una encuesta y aprender sobre recolección y análisis de datos. Este repositorio contiene únicamente el back-end de la aplicación.

## Características

*   API REST para la gestión de encuestas.
*   Cálculo de estadísticas descriptivas.
*   Generación de reportes.
*   Envío de correos electrónicos.

## Tecnologías Utilizadas

*   **Lenguaje:** Python
*   **Framework:** Flask
*   **Base de datos:** MySQL
*   **Contenerización:** Docker
*   **Librerías:**
    *   Gunicorn
    *   Flask-SQLAlchemy
    *   PyMySQL
    *   Flask-CORS
    *   python-dotenv
    *   Flask-Mail
    *   cryptography
    *   pandas

## Repositorio del Front-end

El front-end de este proyecto fue desarrollado con Vue.js y se encuentra en el siguiente repositorio:
[https://github.com/JoanGarfias/front-encuestas-unistmo](https://github.com/JoanGarfias/front-encuestas-unistmo)

## Instalación y Uso

1.  Clonar el repositorio:
    ```bash
    git clone https://github.com/JoanGarfias/back-encuestas-unistmo.git
    ```
2.  Navegar al directorio del proyecto:
    ```bash
    cd back-encuestas-unistmo
    ```
3.  Crear un archivo `.env` basado en el archivo `.env.example` y configurar las variables de entorno.
4.  Construir y levantar los contenedores de Docker:
    ```bash
    docker-compose up --build
    ```
La aplicación estará disponible en `http://localhost:5000`.
