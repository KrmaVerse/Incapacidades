from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "cambia-esta-clave")

def clean(value, limit=100):
    return (value or "").strip()[:limit]

def build_pdf(data):
    output = BytesIO()
    c = canvas.Canvas(output, pagesize=A4)
    w, h = A4

    # Watermark repeated on the page: the document is explicitly non-official.
    c.saveState()
    c.translate(w / 2, h / 2)
    c.rotate(35)
    c.setFillColor(colors.Color(0.75, 0.10, 0.12, alpha=0.18))
    c.setFont("Helvetica-Bold", 34)
    c.drawCentredString(0, 0, "MUESTRA - SIN VALIDEZ MEDICA")
    c.restoreState()

    c.setFillColor(colors.HexColor("#17152e"))
    c.setFont("Helvetica-Bold", 20)
    c.drawString(48, h - 58, "KARMA FREE")
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#555555"))
    c.drawString(48, h - 76, "Generador de documentos de demostracion")
    c.setStrokeColor(colors.HexColor("#6b55c7"))
    c.setLineWidth(2)
    c.line(48, h - 91, w - 48, h - 91)

    c.setFillColor(colors.HexColor("#17152e"))
    c.setFont("Helvetica-Bold", 16)
    c.drawString(48, h - 130, "CONSTANCIA FICTICIA DE REPOSO")
    c.setFillColor(colors.HexColor("#a01818"))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(48, h - 151, "DOCUMENTO DE EJEMPLO - NO ES UNA INCAPACIDAD MEDICA")

    y = h - 195
    rows = [
        ("Nombre ficticio", data["name"]),
        ("Identificacion ficticia", data["document"]),
        ("Fecha de inicio", data["start"]),
        ("Fecha de finalizacion", data["end"]),
        ("Dias indicados en este ejemplo", data["days"]),
        ("Motivo ficticio", data["reason"]),
    ]
    for label, value in rows:
        c.setFillColor(colors.HexColor("#444444"))
        c.setFont("Helvetica-Bold", 10)
        c.drawString(48, y, label + ":")
        c.setFont("Helvetica", 11)
        c.drawString(205, y, value or "No especificado")
        y -= 30

    c.setStrokeColor(colors.HexColor("#bbbbbb"))
    c.line(48, y - 5, w - 48, y - 5)
    y -= 35
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.HexColor("#a01818"))
    c.drawString(48, y, "AVISO IMPORTANTE")
    y -= 20
    c.setFillColor(colors.HexColor("#333333"))
    c.setFont("Helvetica", 9)
    notice = [
        "Este archivo es una plantilla ficticia para pruebas, capacitacion o demostracion.",
        "No acredita enfermedad, consulta, diagnostico ni incapacidad laboral.",
        "No ha sido expedido ni firmado por un profesional o institucion de salud.",
        "No debe presentarse a empleadores, EPS, IPS, aseguradoras ni entidades publicas",
        "como soporte medico o documento autentico."
    ]
    for line in notice:
        c.drawString(48, y, line)
        y -= 15

    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(colors.HexColor("#a01818"))
    c.drawCentredString(w / 2, 45, "MUESTRA - SIN VALIDEZ MEDICA - MUESTRA - SIN VALIDEZ MEDICA")
    c.showPage()
    c.save()
    output.seek(0)
    return output

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = {
            "name": clean(request.form.get("name"), 80),
            "document": clean(request.form.get("document"), 40),
            "start": clean(request.form.get("start"), 20),
            "end": clean(request.form.get("end"), 20),
            "days": clean(request.form.get("days"), 10),
            "reason": clean(request.form.get("reason"), 120),
        }
        if not data["name"] or not data["start"] or not data["end"]:
            flash("Completa al menos el nombre ficticio y las fechas.")
            return redirect(url_for("index"))
        pdf = build_pdf(data)
        return send_file(pdf, as_attachment=True, download_name="muestra_sin_validez_medica.pdf",
                         mimetype="application/pdf")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
