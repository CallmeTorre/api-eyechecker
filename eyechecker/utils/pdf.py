from datetime import datetime
from dateutil.relativedelta import relativedelta

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter

EYES = {'left_eye': 'Izquierdo',
        'right_eye': 'Derecho'}

def create_pdf(pdf_name, title, result, patient_info):
    width, height = letter
    pdf = Canvas(pdf_name, pagesize=letter)
    pdf.setTitle(title)
    for key, value in result.items():
        if value != {}:
            pdf.drawString(420, height-100, "Fecha: " + datetime.now().strftime("%d/%m/%Y"))
            pdf.drawString(80, height-140, "Nombre del Paciente: " + patient_info['nombre'])
            pdf.drawString(80, height-180, "Fecha de nacimiento: " + patient_info['fecha_nacimiento'].strftime("%d/%m/%Y"))
            pdf.drawString(405, height-180, "Edad: " + str(relativedelta(datetime.now(), patient_info['fecha_nacimiento']).years) + " años"),
            pdf.drawString(80, height-220, "Genero: " + patient_info['genero'])
            pdf.drawString(80, height-260, "Ojo analizado: " + EYES[key])
            pdf.drawString(80, height-300, "Conclusión: " + value['conclusion'])
            pdf.drawInlineImage(value["original"], 80, height-500, 200, 150)
            pdf.drawString(130,height-515,"Imagen Original")
            pdf.drawInlineImage(value["exudates"], 320, height-500, 200, 150)
            pdf.drawString(360,height-515,"Detección de Exudados")
            pdf.drawInlineImage(value["hemorrhages"], 80, height- 700, 200, 150)
            pdf.drawString(110,height-715,"Detección de Hemorragias")
            pdf.drawInlineImage(value["micros"], 320, height - 700, 200, 150)
            pdf.drawString(335,height-715,"Detección de Microaneurismas")
            pdf.showPage()
    pdf.save()