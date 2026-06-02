from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8438749703:AAEG9LuBBYfWbd2ekJJFfD3mJA1zmv1JFL0"

# ---------------- WELCOME + MENU ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [

        [
            InlineKeyboardButton("🛡️ Admin", callback_data='admin'),
            InlineKeyboardButton("🌊 Antiflood", callback_data='antiflood'),
            InlineKeyboardButton("🚨 AntiRaid", callback_data='antiraid')
        ],

        [
            InlineKeyboardButton("✅ Approval", callback_data='approval'),
            InlineKeyboardButton("⛔ Bans", callback_data='bans'),
            InlineKeyboardButton("🚫 Blocklists", callback_data='blocklists')
        ],

        [
            InlineKeyboardButton("🧪 CAPTCHA", callback_data='captcha'),
            InlineKeyboardButton("🧹 Clean Commands", callback_data='cleancommands'),
            InlineKeyboardButton("🧼 Clean Service", callback_data='cleanservice')
        ],

        [
            InlineKeyboardButton("🔗 Connections", callback_data='connections'),
            InlineKeyboardButton("🔕 Disabling", callback_data='disabling'),
            InlineKeyboardButton("🌐 Federations", callback_data='federations')
        ],

        [
            InlineKeyboardButton("🧲 Filters", callback_data='filters'),
            InlineKeyboardButton("🎨 Formatting", callback_data='formatting'),
            InlineKeyboardButton("👋 Greetings", callback_data='greetings')
        ],

        [
            InlineKeyboardButton("📦 Import/Export", callback_data='importexport'),
            InlineKeyboardButton("🗣️ Languages", callback_data='languages'),
            InlineKeyboardButton("🔒 Locks", callback_data='locks')
        ],

        [
            InlineKeyboardButton("📋 Log Channels", callback_data='logchannels'),
            InlineKeyboardButton("✨ Misc", callback_data='misc'),
            InlineKeyboardButton("📝 Notes", callback_data='notes')
        ],

        [
            InlineKeyboardButton("📌 Pin", callback_data='pin'),
            InlineKeyboardButton("🔐 Privacy", callback_data='privacy'),
            InlineKeyboardButton("🧽 Purges", callback_data='purges')
        ],

        [
            InlineKeyboardButton("📣 Reports", callback_data='reports'),
            InlineKeyboardButton("📜 Rules", callback_data='rules'),
            InlineKeyboardButton("🧩 Topics", callback_data='topics')
        ],

        [
            InlineKeyboardButton("⚠️ Warnings", callback_data='warnings'),
            InlineKeyboardButton("⭐ Custom Instances", callback_data='custominstances')
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # 👉 WELCOME MESSAGE
    await update.message.reply_text(
        "🛡️ Welcome to Bright Security Bot\n\n"
        "I help you manage and secure your group efficiently.\n\n"
        "⚙️ Use the buttons below to access all features.",
        reply_markup=reply_markup
    )

# ---------------- BUTTON HANDLER ----------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    await query.edit_message_text(f"⚙️ {data.upper()} module opened")

# ---------------- RUN BOT ----------------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("Bright Security Bot Running...")
app.run_polling()
