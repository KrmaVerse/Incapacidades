import os
from io import BytesIO
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from app import build_pdf

HELP = (
    "Soy el generador de muestras de Karma Free.\n\n"
    "Envíame los datos en este orden, separados por |:\n"
    "Nombre ficticio | ID ficticia | Fecha inicio | Fecha fin | Días | Motivo ficticio\n\n"
    "Ejemplo:\n"
    "Alex Demo | 000000 | 2026-11-06 | 2026-11-07 | 2 | Ejemplo de reposo\n\n"
    "El PDF llevará una marca visible: MUESTRA - SIN VALIDEZ MÉDICA. "
    "No es una incapacidad ni sirve como soporte laboral."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP)

async def make_sample(update: Update, context: ContextTypes.DEFAULT_TYPE):
    parts = [p.strip() for p in update.message.text.split("|")]
    if len(parts) != 6:
        await update.message.reply_text(HELP)
        return
    data = dict(zip(["name", "document", "start", "end", "days", "reason"], parts))
    pdf = build_pdf(data)
    bio = BytesIO(pdf.read())
    bio.name = "muestra_sin_validez_medica.pdf"
    await update.message.reply_document(
        document=bio,
        caption="MUESTRA - SIN VALIDEZ MÉDICA. Documento ficticio para demostración; no acredita incapacidad."
    )

def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("Configura TELEGRAM_BOT_TOKEN en las variables de entorno.")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, make_sample))
    app.run_polling()

if __name__ == "__main__":
    main()
