from logging import info
from pathlib import Path
from datetime import datetime
from os import getcwd, path, getenv, remove
from dateutil.relativedelta import relativedelta

from boto3 import client
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter

EYES = {'left_eye': 'Izquierdo',
        'right_eye': 'Derecho'}

def get_pdf_url(url):
    s3 = client(
            "s3",
            aws_access_key_id=getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=getenv('AWS_SECRET_ACCESS_KEY'))
    response = s3.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': getenv('BUCKET_NAME'),
            'Key': url},
        ExpiresIn=3600)
    return response

def upload_pdf_s3(id_paciente, pdf_name):
    info('Subiendo el reporte')
    s3 = client(
            "s3",
            aws_access_key_id=getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=getenv('AWS_SECRET_ACCESS_KEY'))
    s3.upload_file(
        Bucket=getenv('BUCKET_NAME'),
        Filename=pdf_name,
        Key=str(id_paciente) + "/" + pdf_name
    )
    info('Reporte subido')


def create_pdf(result, patient_info):
    info("Creando reporte")
    current_path = Path(getcwd())
    pdf_name = datetime.now().strftime("%d%m%Y%H%M%S") + ".pdf"
    title = "Reporte del paciente: " + patient_info['nombre']
    width, height = letter
    pdf = Canvas(pdf_name, pagesize=letter)
    pdf.setTitle(title)
    for key, value in result.items():
        if value != {}:
            pdf.drawString(420, height-100, "Fecha: " + datetime.now().strftime("%d/%m/%Y"))
            pdf.drawString(80, height-140, "Nombre del Paciente: " + patient_info['nombre'])
            pdf.drawString(80, height-180, "Fecha de nacimiento: " + patient_info['fecha_nacimiento'])
            pdf.drawString(405, height-180, "Edad: " + str(relativedelta(datetime.now(), datetime.strptime(patient_info['fecha_nacimiento'], '%d-%m-%Y')).years) + " años"),
            pdf.drawString(80, height-220, "Genero: " + patient_info['genero'])
            pdf.drawString(80, height-260, "Ojo analizado: " + EYES[key])
            pdf.drawString(80, height-300, "Conclusión: " + value['conclusion'])
            pdf.drawInlineImage(value["original"], 80, height-500, 200, 150)
            remove(value["original"])
            pdf.drawString(130,height-515,"Imagen Original")
            pdf.drawInlineImage(value["exudates"], 320, height-500, 200, 150)
            remove(value["exudates"])
            pdf.drawString(360,height-515,"Detección de Exudados")
            pdf.drawInlineImage(value["hemorrhages"], 80, height- 700, 200, 150)
            remove(value["hemorrhages"])
            pdf.drawString(110,height-715,"Detección de Hemorragias")
            pdf.drawInlineImage(value["micros"], 320, height - 700, 200, 150)
            remove(value["micros"])
            pdf.drawString(335,height-715,"Detección de Microaneurismas")
            pdf.showPage()
    pdf.save()
    info("Reporte creado")
    #upload_pdf_s3(patient_info['id_paciente'], pdf_name)
    #info("Borrando reporte")
    #remove(pdf_name)
    #info("Reporte borrado")
    return path.join(current_path, pdf_name)