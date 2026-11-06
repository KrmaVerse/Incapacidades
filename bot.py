import os
from io import BytesIO
from datetime import date
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters
from app import build_pdf

NAME,DOC,START,END,REASON=range(5)
MENU=ReplyKeyboardMarkup([[KeyboardButton("Crear documento de demostracion")],[KeyboardButton("Ayuda"),KeyboardButton("Cancelar")]],resize_keyboard=True)
INTRO=("Karma Free genera solo documentos ficticios de demostracion con marca permanente "
       "MUESTRA - SIN VALIDEZ MEDICA. No son incapacidades ni soportes laborales.")

async def start(update:Update, context:ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(INTRO+"\n\nPulsa «Crear documento de demostracion».",reply_markup=MENU)
    return ConversationHandler.END

async def begin(update:Update,context:ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("Escribe un nombre ficticio.")
    return NAME

async def name_step(update,context):
    v=update.message.text.strip()
    if len(v)<2 or len(v)>80:
        await update.message.reply_text("Escribe un nombre de ejemplo de 2 a 80 caracteres."); return NAME
    context.user_data["name"]=v
    await update.message.reply_text("Escribe una identificacion ficticia (ejemplo 000000).")
    return DOC

async def doc_step(update,context):
    context.user_data["document"]=update.message.text.strip()[:40]
    await update.message.reply_text("Fecha de inicio en formato AAAA-MM-DD. Ejemplo: 2026-11-06")
    return START

def parse_date(s):
    try: return date.fromisoformat(s.strip())
    except ValueError: return None

async def start_step(update,context):
    d=parse_date(update.message.text)
    if not d:
        await update.message.reply_text("Fecha no valida. Usa AAAA-MM-DD."); return START
    context.user_data["start"]=d.isoformat()
    await update.message.reply_text("Fecha de finalizacion en formato AAAA-MM-DD.")
    return END

async def end_step(update,context):
    d=parse_date(update.message.text); s=parse_date(context.user_data["start"])
    if not d or d<s:
        await update.message.reply_text("Fecha no valida o anterior al inicio. Intenta de nuevo (AAAA-MM-DD)."); return END
    context.user_data["end"]=d.isoformat()
    context.user_data["days"]=str((d-s).days+1)
    await update.message.reply_text("Escribe un motivo ficticio (maximo 120 caracteres).")
    return REASON

async def reason_step(update,context):
    v=update.message.text.strip()
    if not v or len(v)>120:
        await update.message.reply_text("Escribe un texto de hasta 120 caracteres."); return REASON
    context.user_data["reason"]=v
    pdf=build_pdf(context.user_data); f=BytesIO(pdf.read()); f.name="KarmaFree_MUESTRA_SIN_VALIDEZ_MEDICA.pdf"
    await update.message.reply_document(document=f,caption="MUESTRA - SIN VALIDEZ MEDICA. Documento ficticio; no es una incapacidad ni soporte laboral.")
    context.user_data.clear()
    await update.message.reply_text("PDF de demostracion generado. Puedes crear otro desde el menu.",reply_markup=MENU)
    return ConversationHandler.END

async def cancel(update,context):
    context.user_data.clear()
    await update.message.reply_text("Proceso cancelado.",reply_markup=MENU)
    return ConversationHandler.END

async def help_cmd(update,context):
    await update.message.reply_text(INTRO+"\nPulsa el boton para comenzar.",reply_markup=MENU)

def main():
    token=os.getenv("TELEGRAM_BOT_TOKEN")
    if not token: raise RuntimeError("Falta TELEGRAM_BOT_TOKEN en Railway.")
    app=Application.builder().token(token).build()
    conv=ConversationHandler(
      entry_points=[MessageHandler(filters.Regex(r"^Crear documento de demostracion$"),begin)],
      states={
        NAME:[MessageHandler(filters.TEXT & ~filters.COMMAND,name_step)],
        DOC:[MessageHandler(filters.TEXT & ~filters.COMMAND,doc_step)],
        START:[MessageHandler(filters.TEXT & ~filters.COMMAND,start_step)],
        END:[MessageHandler(filters.TEXT & ~filters.COMMAND,end_step)],
        REASON:[MessageHandler(filters.TEXT & ~filters.COMMAND,reason_step)]
      },
      fallbacks=[CommandHandler("cancel",cancel),MessageHandler(filters.Regex(r"^Cancelar$"),cancel)],
      allow_reentry=True)
    app.add_handler(CommandHandler("start",start))
    app.add_handler(CommandHandler("help",help_cmd))
    app.add_handler(conv)
    app.add_handler(MessageHandler(filters.Regex(r"^Ayuda$"),help_cmd))
    print("Karma Free demo bot iniciado; esperando mensajes.",flush=True)
    app.run_polling(drop_pending_updates=True)

if __name__=="__main__": main()
