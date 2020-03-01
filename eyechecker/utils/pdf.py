from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter

def create_pdf(pdf_name, title, result):
    width, height = letter
    pdf = Canvas(pdf_name, pagesize=letter)
    pdf.setTitle(title)
    pdf.drawInlineImage(result['left_eye']["original"], 80, height-500, 200, 150)
    pdf.drawInlineImage(result['left_eye']["exudates"], 320, height-500, 200, 150)
    pdf.drawInlineImage(result['left_eye']["hemorrhages"], 80, height- 700, 200, 150)
    pdf.drawInlineImage(result['left_eye']["micros"], 320, height - 700, 200, 150)
    pdf.showPage()
    pdf.save()