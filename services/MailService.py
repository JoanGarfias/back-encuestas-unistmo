from flask_mail import Message
from extensions import mail # Importamos la instancia de mail y la app
from flask import current_app

def enviar_correo_simple(recipient: str, subject: str, body: str):
    """
    Función para construir y enviar un correo electrónico.
    """
    try:
        msg = Message(
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            subject=subject,
            recipients=[recipient],
            body=body
            # html="<h1>Cuerpo en HTML</h1>" # Usa 'html' en lugar de 'body' para HTML
        )

        mail.send(msg)

        return True, "Correo enviado con éxito."
    except Exception as e:
        print(f"ERROR AL ENVIAR CORREO: {e}")
        return False, str(e)
