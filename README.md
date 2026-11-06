# Karma Free — Generador de documentos de demostración

Proyecto inicial con:
- Página web Flask para generar un PDF ficticio.
- Bot de Telegram para generar el mismo PDF mediante un mensaje con campos.
- Marca de agua y avisos permanentes: **MUESTRA — SIN VALIDEZ MÉDICA**.

## Límites de uso
Esta aplicación no genera incapacidades médicas auténticas. No incluye logos de EPS/IPS, firmas, sellos, códigos de validación ni datos de profesionales. Usa únicamente datos ficticios y no presentes sus resultados como soportes laborales.

## Requisitos
- Python 3.10 o superior
- Una cuenta de Telegram y un bot creado con BotFather (solo si usarás el bot)

## Instalación
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecutar la página web
```bash
python app.py
```
Abre `http://127.0.0.1:5000`.

## Ejecutar el bot de Telegram
1. Crea un bot con `@BotFather` y copia su token.
2. Configura la variable de entorno `TELEGRAM_BOT_TOKEN`.
3. Ejecuta:
```bash
python bot.py
```

En Windows PowerShell:
```powershell
$env:TELEGRAM_BOT_TOKEN="TU_TOKEN"
python bot.py
```

En Linux/macOS:
```bash
export TELEGRAM_BOT_TOKEN="TU_TOKEN"
python bot.py
```

## Formato para Telegram
Envía seis campos separados por `|`:
`Nombre ficticio | ID ficticia | Fecha inicio | Fecha fin | Días | Motivo ficticio`

Ejemplo:
`Alex Demo | 000000 | 2026-11-06 | 2026-11-07 | 2 | Ejemplo de reposo`

## Publicación
Para publicar la web, usa un hosting compatible con Python/Flask y configura `FLASK_SECRET`.
No publiques el token del bot ni lo subas a GitHub. Añade autenticación y límites de uso antes de abrir el servicio al público.
