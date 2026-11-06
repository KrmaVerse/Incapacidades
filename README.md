# Karma Free V2 - Bot automatico de demostracion

Esta version usa botones y preguntas paso a paso; ya no requiere separar datos con `|`.
Genera un PDF ficticio con marca permanente MUESTRA - SIN VALIDEZ MEDICA.
No genera incapacidades reales ni soportes laborales, ni imita EPS/IPS, firmas, sellos o codigos oficiales.

## Actualizar Railway
1. Reemplaza `bot.py`, `app.py` y `requirements.txt` en la raiz del repositorio GitHub.
2. Haz Commit changes.
3. En Railway confirma Start Command: `python bot.py`.
4. Conserva la variable `TELEGRAM_BOT_TOKEN` (no la publiques).
5. Espera el nuevo deploy. En logs debe aparecer: `Karma Free demo bot iniciado; esperando mensajes.`
6. En Telegram envia `/start`, pulsa `Crear documento de demostracion` y sigue las preguntas.

No ejecutes el mismo token en dos servicios simultaneamente: puede causar conflicto de polling.
