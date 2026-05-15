import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "TON_TOKEN_ICI"
TON_ID = 8723770508  # Ton ID Telegram perso

logging.basicConfig(level=logging.INFO)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👗 Bonjour et bienvenue !\n\n"
        "Je suis là pour vous aider avec nos produits.\n\n"
        "👉 Quel produit vous intéresse ?"
    )

# /delais
async def delais(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📦 Nos délais de livraison :\n\n"
        "• Colissimo : 2-3 jours ouvrés\n"
        "• Mondial Relay : 3-5 jours ouvrés\n"
        "• International : 18-20 jours ouvrés\n\n"
        "Des questions ? Dites-nous quel produit vous intéresse 😊"
    )

# Messages libres des clients
async def repondre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    client = update.message.from_user
    prenom = client.first_name or "Client"
    message = update.message.text
    client_id = client.id

    # Réponse automatique au client
    await update.message.reply_text(
        f"Merci {prenom} ! 🙏\n\n"
        "Nous avons bien reçu votre demande.\n"
        "On revient vers vous très vite avec le prix ! ⏳"
    )

    # Alerte à toi
    await context.bot.send_message(
        chat_id=TON_ID,
        text=(
            f"🔔 Nouvelle demande client !\n\n"
            f"👤 Prénom : {prenom}\n"
            f"🆔 ID : {client_id}\n"
            f"💬 Message : {message}\n\n"
            f"👉 Pour lui répondre, utilise la commande :\n"
            f"/repondre {client_id} Ton message ici"
        )
    )

# Toi tu réponds à un client via /repondre <id> <message>
async def repondre_client(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != TON_ID:
        return  # Sécurité : seul toi peux utiliser cette commande

    if len(context.args) < 2:
        await update.message.reply_text(
            "❌ Format : /repondre <ID_client> <ton message>\n"
            "Exemple : /repondre 123456789 La robe fleurie est à 35€ 😊"
        )
        return

    client_id = int(context.args[0])
    message = " ".join(context.args[1:])

    await context.bot.send_message(
        chat_id=client_id,
        text=f"👗 Réponse de notre équipe :\n\n{message}\n\nDes questions ? On est là ! 😊"
    )
    await update.message.reply_text("✅ Message envoyé au client !")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("delais", delais))
app.add_handler(CommandHandler("repondre", repondre_client))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, repondre))

print("✅ Bot démarré !")
app.run_polling()
