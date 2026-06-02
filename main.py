from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8438749703:AAEG9LuBBYfWbd2ekJJFfD3mJA1zmv1JFL0"

# ---------------- FULL MAIN MENU (28 BUTTONS, 3 per row) ----------------
def main_menu():
    return InlineKeyboardMarkup([

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
            InlineKeyboardButton("🧹 Clean Cmd", callback_data='cleancommands'),
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
    ])

# ---------------- BACK BUTTON ----------------
def back_btn():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Back", callback_data='back')]
    ])

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛡️ Welcome to Security Bot\n\nChoose a module:",
        reply_markup=main_menu()
    )

# ---------------- BUTTON HANDLER ----------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back":
        await query.edit_message_text("🛡️ Main Menu", reply_markup=main_menu())

    elif data == "admin":
        await query.edit_message_text("🛡️ Admin Panel\n/promote /demote /ban /unban", reply_markup=back_btn())

    elif data == "antiflood":
        await query.edit_message_text("🌊 AntiFlood System Active", reply_markup=back_btn())

    elif data == "antiraid":
        await query.edit_message_text("🚨 AntiRaid Protection ON", reply_markup=back_btn())

    elif data == "bans":
        await query.edit_message_text("⛔ Ban System Ready", reply_markup=back_btn())

    elif data == "blocklists":
        await query.edit_message_text("🚫 Blocklist System Active", reply_markup=back_btn())

    elif data == "captcha":
        await query.edit_message_text("🧪 CAPTCHA Enabled", reply_markup=back_btn())

    elif data == "cleancommands":
        await query.edit_message_text("🧹 Clean Commands ON", reply_markup=back_btn())

    elif data == "cleanservice":
        await query.edit_message_text("🧼 Clean Service ON", reply_markup=back_btn())

    elif data == "connections":
        await query.edit_message_text("🔗 Connections System", reply_markup=back_btn())

    elif data == "disabling":
        await query.edit_message_text("🔕 Disabling Commands", reply_markup=back_btn())

    elif data == "federations":
        await query.edit_message_text("🌐 Federation System", reply_markup=back_btn())

    elif data == "filters":
        await query.edit_message_text("🧲 Filters Active", reply_markup=back_btn())

    elif data == "formatting":
        await query.edit_message_text("🎨 Formatting Tools", reply_markup=back_btn())

    elif data == "greetings":
        await query.edit_message_text("👋 Greetings System", reply_markup=back_btn())

    elif data == "importexport":
        await query.edit_message_text("📦 Import/Export System", reply_markup=back_btn())

    elif data == "languages":
        await query.edit_message_text("🗣️ Language Settings", reply_markup=back_btn())

    elif data == "locks":
        await query.edit_message_text("🔒 Locks System", reply_markup=back_btn())

    elif data == "logchannels":
        await query.edit_message_text("📋 Log Channels", reply_markup=back_btn())

    elif data == "misc":
        await query.edit_message_text("✨ Misc Tools", reply_markup=back_btn())

    elif data == "notes":
        await query.edit_message_text("📝 Notes System", reply_markup=back_btn())

    elif data == "pin":
        await query.edit_message_text("📌 Pin System", reply_markup=back_btn())

    elif data == "privacy":
        await query.edit_message_text("🔐 Privacy Settings", reply_markup=back_btn())

    elif data == "purges":
        await query.edit_message_text("🧽 Purge System", reply_markup=back_btn())

    elif data == "reports":
        await query.edit_message_text("📣 Reports System", reply_markup=back_btn())

    elif data == "rules":
        await query.edit_message_text("📜 Rules System", reply_markup=back_btn())

    elif data == "topics":
        await query.edit_message_text("🧩 Topics System", reply_markup=back_btn())

    elif data == "warnings":
        await query.edit_message_text("⚠️ Warning System", reply_markup=back_btn())

    elif data == "custominstances":
        await query.edit_message_text("⭐ Custom Instances", reply_markup=back_btn())

# ---------------- APP ----------------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("Bot Running...")
app.run_polling()
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "YOUR_BOT_TOKEN"

# ---------------- MEMORY ----------------
filters_db = {}
warn_db = {}

# ---------------- UTIL ----------------
def format_text(text, user):
    return text.replace("{first}", user.first_name or "") \
               .replace("{username}", "@" + user.username if user.username else user.first_name)

# ---------------- FILTER SET ----------------
async def set_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        return await update.message.reply_text("Usage: /filter hello hello {first} how are you")

    keyword = context.args[0].lower()
    reply = " ".join(context.args[1:])

    filters_db[update.effective_chat.id, keyword] = reply
    await update.message.reply_text(f"✅ Filter set for '{keyword}'")

# ---------------- REMOVE FILTER ----------------
async def stop_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /stop hello")

    keyword = context.args[0].lower()
    key = (update.effective_chat.id, keyword)

    if key in filters_db:
        del filters_db[key]
        await update.message.reply_text("❌ Filter removed")
    else:
        await update.message.reply_text("Not found")

# ---------------- MESSAGE CHECK (AUTO REPLY ENGINE) ----------------
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    text = update.message.text.lower()
    chat_id = update.effective_chat.id
    user = update.message.from_user

    for (cid, keyword), reply in filters_db.items():
        if cid == chat_id and keyword in text:
            final_text = format_text(reply, user)
            await update.message.reply_text(final_text)

# ---------------- BAN ----------------
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("Reply to user")

    uid = update.message.reply_to_message.from_user.id
    await context.bot.ban_chat_member(update.effective_chat.id, uid)
    await update.message.reply_text("🚫 User banned")

# ---------------- MUTE ----------------
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("Reply to user")

    uid = update.message.reply_to_message.from_user.id

    await context.bot.restrict_chat_member(
        update.effective_chat.id,
        uid,
        ChatPermissions(can_send_messages=False)
    )

    await update.message.reply_text("🔇 User muted")

# ---------------- UNMUTE ----------------
async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("Reply to user")

    uid = update.message.reply_to_message.from_user.id

    await context.bot.restrict_chat_member(
        update.effective_chat.id,
        uid,
        ChatPermissions(can_send_messages=True)
    )

    await update.message.reply_text("🔊 User unmuted")

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛡️ Rose Engine Active\n\n"
        "Commands:\n"
        "/filter keyword reply\n"
        "/stop keyword\n"
        "/ban (reply)\n"
        "/mute /unmute"
    )

# ---------------- APP ----------------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

# FILTER SYSTEM
app.add_handler(CommandHandler("filter", set_filter))
app.add_handler(CommandHandler("stop", stop_filter))

# MODERATION
app.add_handler(CommandHandler("ban", ban))
app.add_handler(CommandHandler("mute", mute))
app.add_handler(CommandHandler("unmute", unmute))

# AUTO MESSAGE ENGINE
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

print("🚀 Rose Engine Running...")
app.run_polling()
