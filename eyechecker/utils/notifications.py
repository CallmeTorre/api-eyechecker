import logging
from os import getenv

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_recover_email(email):
    """
    Function that sends an email to recover the password.
    """
    message = Mail(
        from_email=getenv('SENDER_EMAIL'),
        to_emails=email,
        subject='Recuperación de Contraseña',
        html_content='<p>Porfavor acceda a este link para reiniciar su contraseña</p>')
    try:
        sg = SendGridAPIClient(getenv('SENDGRID_API_KEY'))
        response = sg.send(message)
        logging.info(response.status_code)
        logging.info(response.body)
        logging.info(response.headers)
        return {'status': 'Mensaje enviado correctamente'}, 200
    except Exception as e:
        logging.warn(e.message)
        logging.warn(response.status_code)
        logging.warn(response.body)
        logging.warn(response.headers)
        return {'error': 'No se pudo enviar el mensaje, intente mas tarde'}, response.status_code