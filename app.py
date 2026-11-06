from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def build_pdf(data):
    out = BytesIO()
    c = canvas.Canvas(out, pagesize=A4)
    w, h = A4
    c.saveState()
    c.translate(w/2, h/2); c.rotate(35)
    c.setFillColor(colors.Color(.78, .08, .12, alpha=.22))
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(0, 0, "MUESTRA - SIN VALIDEZ MEDICA")
    c.restoreState()
    c.setFillColor(colors.HexColor("#17152e"))
    c.setFont("Helvetica-Bold", 22); c.drawString(48, h-58, "KARMA FREE")
    c.setFont("Helvetica", 10); c.drawString(48, h-77, "Documento ficticio para demostracion")
    c.setStrokeColor(colors.HexColor("#7655d9")); c.setLineWidth(2); c.line(48,h-91,w-48,h-91)
    c.setFont("Helvetica-Bold", 16); c.drawString(48,h-128,"CONSTANCIA FICTICIA DE REPOSO")
    c.setFillColor(colors.HexColor("#a01818")); c.setFont("Helvetica-Bold",10)
    c.drawString(48,h-149,"NO ES UNA INCAPACIDAD MEDICA NI UN SOPORTE LABORAL")
    y=h-195
    for label,key in [("Nombre de ejemplo","name"),("Identificacion ficticia","document"),("Fecha de inicio","start"),("Fecha de finalizacion","end"),("Duracion de ejemplo","days"),("Motivo ficticio","reason")]:
        c.setFillColor(colors.HexColor("#444444")); c.setFont("Helvetica-Bold",10); c.drawString(48,y,label+":")
        c.setFont("Helvetica",11); c.drawString(205,y,str(data.get(key,""))[:90]); y-=29
    y-=10; c.setStrokeColor(colors.grey); c.line(48,y,w-48,y); y-=28
    c.setFillColor(colors.HexColor("#a01818")); c.setFont("Helvetica-Bold",10); c.drawString(48,y,"AVISO PERMANENTE")
    y-=18; c.setFillColor(colors.HexColor("#333333")); c.setFont("Helvetica",9)
    for line in ["Plantilla ficticia para pruebas o demostraciones.","No acredita consulta, enfermedad, diagnostico ni incapacidad laboral.","No ha sido expedida ni validada por profesional o institucion de salud.","No debe presentarse ante empleadores, EPS, IPS o entidades publicas."]:
        c.drawString(48,y,line); y-=15
    c.setFillColor(colors.HexColor("#a01818")); c.setFont("Helvetica-Bold",9)
    c.drawCentredString(w/2,43,"MUESTRA - SIN VALIDEZ MEDICA")
    c.save(); out.seek(0); return out
