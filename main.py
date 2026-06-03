from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, 
    MessageHandler, ContextTypes, filters
)

TOKEN = "8438749703:AAEG9LuBBYfWbd2ekJJFfD3mJA1zmv1JFL0"

# ---------------- MODULE MEMORY (DATABASES) ----------------
filters_db = {}
welcome_db = {}
goodbye_db = {}
warn_db = {}
rules_db = {}

DEFAULT_WELCOME = "Welcome {first} to our group {chatname}!"
DEFAULT_GOODBYE = "👋 Goodbye {first}, we will miss you in {chatname}."

# ---------------- HELPER FUNCTIONS ----------------
def format_text(text, user, chat=None):
    formatted = text.replace("{first}", user.first_name or "") \
                    .replace("{username}", "@" + user.username if user.username else user.first_name)
    if chat:
        formatted = formatted.replace("{chatname}", chat.title or "this group")
    return formatted

async def check_admin(chat_id, user_id, bot):
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status in ['administrator', 'creator']
    except:
        return False

# ---------------- FULL MAIN MENU (ALL 29 BUTTONS) ----------------
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

def back_btn():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Back", callback_data='back_main')]
    ])

# ---------------- ALL 29 MODULE RESPONSES Complete ----------------
MODULE_RESPONSES = {
    "admin": "🛡️ *Admin Module*\n\nManage your group administrators. Use commands like /promote or /demote to grant or remove admin rights.",
    "antiflood": "🌊 *Anti-Flood Protection*\n\nPrevent users from spamming multiple messages quickly. Configure limit settings here to auto-mute spammers.",
    "antiraid": "🚨 *Anti-Raid System*\n\nLock down your group instantly during a mass join attack or automated bot raid.",
    "approval": "✅ *Member Approval*\n\nRequire manual admin approval or custom verification questions for new members before they can chat.",
    "bans": "⛔ *Ban Settings*\n\nManage banned users, kick problematic accounts, or check the global ban configuration.",
    "blocklists": "🚫 *Blocklists & Word Filters*\n\nAdd restricted words, links, or custom phrases that should be automatically deleted by the bot.",
    "captcha": "🧪 *CAPTCHA Verification*\n\nEnable image, text, or button CAPTCHAs to stop automated bot accounts from joining your group.",
    "cleancommands": "🧹 *Clean Commands*\n\nAutomatically delete bot invocation commands (like /help, /start) after a few seconds to keep the chat clean.",
    "cleanservice": "🧼 *Clean Service Messages*\n\nAutomatically remove system messages like 'User joined' or 'User left' to avoid chat clutter.",
    "connections": "🔗 *Group Connections*\n\nConnect multiple groups together to sync configuration settings or manage them from a single dashboard.",
    "disabling": "🔕 *Disable Commands*\n\nTurn off specific bot commands entirely or restrict them to group administrators only.",
    "federations": "🌐 *Federation System*\n\nJoin a shared ban network across multiple groups to ban known scammers and spammers instantly.",
    "filters": "🧲 *Custom Filters*\n\nSet up custom automated replies for specific trigger keywords sent by group members.",
    "formatting": "🎨 *Text Formatting*\n\nConfigure custom styling, markdown support, or bold/italic settings for all bot generated messages.",
    "greetings": "👋 *Greetings & Welcomes*\n\nCustomize premium welcome messages and goodbye alerts for your group members.",
    "importexport": "📦 *Import/Export Settings*\n\nBackup your entire group configuration or import preset security settings from another group.",
    "languages": "🗣️ *Language Settings*\n\nChange the default operational language of Bright Security Bot.",
    "locks": "🔒 *Chat Locks*\n\nLock down specific media types such as voice notes, stickers, links, gifs, or games in the group chat.",
    "logchannels": "📋 *Log Channels*\n\nForward all moderation actions, warnings, and deleted messages to a private log channel.",
    "misc": "✨ *Miscellaneous Tools*\n\nAccess additional utility features, user lookup tools, and extra commands.",
    "notes": "📝 *Group Notes*\n\nSave important messages, links, or instructions as notes that members can retrieve using hashtags.",
    "pin": "📌 *Pin Management*\n\nConfigure how the bot handles pinned messages, layout changes, and pin notifications.",
    "privacy": "🔐 *Privacy Settings*\n\nManage data collection preferences, incognito features, or user data visibility settings.",
    "purges": "🧽 *Chat Purge*\n\nQuickly clear thousands of messages in bulk using the advanced /purge command.",
    "reports": "📣 *User Reporting*\n\nAllow group members to report spam or bad behavior directly to admins using @admin or /report.",
    "rules": "📜 *Group Rules*\n\nSet up, update, and display the official rules of your group using the /rules command.",
    "topics": "🧩 *Topic Management*\n\nConfigure security rules and moderation tools specifically designed for Telegram Forum Topics.",
    "warnings": "⚠️ *Warning System*\n\nIssue warnings to rule breakers. Set custom limits (e.g., 3 warnings = automatic temporary ban).",
    "custominstances": "⭐ *Custom Instances*\n\nDeploy a dedicated private version of Bright Security Bot for maximum speed and uptime."
}

# ---------------- CONNECT COMMAND (GROUP ONLY) ----------------
async def connect_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type == 'private':
        return await update.message.reply_text("This command must be used inside a group chat.")
    
    bot_username = context.bot.username
    url = f"https://t.me/{bot_username}?start={chat.id}"
    
    keyboard = [[InlineKeyboardButton("चैट से कनेक्ट करे", url=url)]]
    await update.message.reply_text(
        "पीएम में इस चैट से जुड़ने के लिए निम्न बटन पर टैप करें",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ---------------- START COMMAND (WITH DEEP-LINKING) ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Checking for PM deep-link payload
    if context.args and update.effective_chat.type == 'private':
        try:
            chat_id = int(context.args[0])
            chat = await context.bot.get_chat(chat_id)
            context.user_data['current_chat_id'] = chat_id  # Storing active chat context
            
            is_admin = await check_admin(chat_id, update.effective_user.id, context.bot)
            
            keyboard = []
            if is_admin:
                keyboard.append([InlineKeyboardButton("Admin", callback_data=f'cmd_admin_{chat_id}')])
            keyboard.append([InlineKeyboardButton("User", callback_data=f'cmd_user_{chat_id}')])
            
            await update.message.reply_text(
                f"You have been connected to {chat.title}!",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return
        except Exception:
            pass

    # Standard Main Menu
    await update.message.reply_text(
        "✨ *Welcome to Bright Security Bot* ✨\n\n"
        "🤖 I am your advanced group management and protection companion.\n\n"
        "⚙️ *Choose a module below to configure me:*",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

# ---------------- BUTTON HANDLING ENGINE ----------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back_main":
        await query.edit_message_text(
            "✨ *Main Menu* ✨\n\nChoose a module to configure:", 
            parse_mode="Markdown", reply_markup=main_menu()
        )
    
    elif data in MODULE_RESPONSES:
        await query.edit_message_text(
            MODULE_RESPONSES[data], parse_mode="Markdown", reply_markup=back_btn()
        )

    elif data.startswith("cmd_admin_"):
        chat_id = data.split("_")[2]
        text = (
            "🛡️ *Admin Control Panel Available Commands:*\n\n"
            "• `/setwelcome <msg>` - Setup welcome banner\n"
            "• `/welcome` - View current welcome banner\n"
            "• `/resetwelcome` - Restore default welcome settings\n"
            "• `/setgoodbye <msg>` - Setup goodbye banner\n"
            "• `/goodbye` - View current goodbye banner\n"
            "• `/resetgoodbye` - Restore default goodbye settings\n"
            "• `/filter <trigger> <reply>` - Add dynamic keyword filter\n"
            "• `/stop <trigger>` - Terminate active keyword filter\n"
            "• `/ban` - Restrict target account permanently (Reply required)\n"
            "• `/mute` - Mute account capabilities (Reply required)\n"
            "• `/unmute` - Revoke account mute restrictions (Reply required)"
        )
        keyboard = [
            [InlineKeyboardButton("User", callback_data=f'cmd_user_{chat_id}'),
             InlineKeyboardButton("Back", callback_data=f'cmd_back_{chat_id}')]
        ]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("cmd_user_"):
        chat_id = data.split("_")[2]
        text = (
            "👤 *User Utilities Panel Available Commands:*\n\n"
            "• `/rules` - Review official group guidelines\n"
            "• `/adminlist` - Output current group administration team\n"
            "• `/warn` - Review your overall warning count record"
        )
        keyboard = [[InlineKeyboardButton("Back", callback_data=f'cmd_back_{chat_id}')]]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("cmd_back_"):
        chat_id = data.split("_")[2]
        try:
            chat = await context.bot.get_chat(int(chat_id))
            is_admin = await check_admin(int(chat_id), query.from_user.id, context.bot)
            
            keyboard = []
            if is_admin:
                keyboard.append([InlineKeyboardButton("Admin", callback_data=f'cmd_admin_{chat_id}')])
            keyboard.append([InlineKeyboardButton("User", callback_data=f'cmd_user_{chat_id}')])
            
            await query.edit_message_text(
                f"You have been connected to {chat.title}!",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        except:
            await query.edit_message_text("Connection profile closed. Please request /connect from the group.")

# ---------------- OPERATIONAL COMMAND HANDLERS ----------------
async def rules_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id if update.effective_chat.type != 'private' else context.user_data.get('current_chat_id')
    if not chat_id: return await update.message.reply_text("No group linked.")
    rules = rules_db.get(chat_id, "No operational group guidelines have been established yet.")
    await update.message.reply_text(f"📜 *Official Chat Rules:*\n\n{rules}", parse_mode="Markdown")

async def adminlist_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id if update.effective_chat.type != 'private' else context.user_data.get('current_chat_id')
    if not chat_id: return await update.message.reply_text("No group linked.")
    
    admins = await context.bot.get_chat_administrators(chat_id)
    text = "🛡️ *Active Administration Staff:*\n"
    for admin in admins:
        text += f"- @{admin.user.username or admin.user.first_name}\n"
    await update.message.reply_text(text, parse_mode="Markdown")

async def warn_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id if update.effective_chat.type != 'private' else context.user_data.get('current_chat_id')
    if not chat_id: return await update.message.reply_text("No group linked.")
    
    warnings = warn_db.get((chat_id, user_id), 0)
    await update.message.reply_text(f"⚠️ Your account currently holds *{warnings}* warning flags in this chat structure.", parse_mode="Markdown")

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id if update.effective_chat.type != 'private' else context.user_data.get('current_chat_id')
    if not chat_id: return
    if not await check_admin(chat_id, update.effective_user.id, context.bot): return
    if not update.message.reply_to_message: return await update.message.reply_text("Reply to a message to target an account.")

    uid = update.message.reply_to_message.from_user.id
    try:
        await context.bot.ban_chat_member(chat_id, uid)
        await update.message.reply_text("🚫 Target account has been restricted successfully.")
    except:
        await update.message.reply_text("❌ Action failed. Verify bot administrator privilege rights.")

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id if update.effective_chat.type != 'private' else context.user_data.get('current_chat_id')
    if not chat_id: return
    if not await check_admin(chat_id, update.effective_user.id, context.bot): return
    if not update.message.reply_to_message: return await update.message.reply_text("Reply to a message to target an account.")

    uid = update.message.reply_to_message.from_user.id
    try:
        await context.bot.restrict_chat_member(chat_id, uid, ChatPermissions(can_send_messages=False))
        await update.message.reply_text("危害 Restricted communication permissions applied successfully.")
    except:
        await update.message.reply_text("❌ Action failed. Verify bot administrator privilege rights.")

async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id if update.effective_chat.type != 'private' else context.user_data.get('current_chat_id')
    if not chat_id: return
    if not await check_admin(chat_id, update.effective_user.id, context.bot): return
    if not update.message.reply_to_message: return

    uid = update.message.reply_to_message.from_user.id
    try:
        await context.bot.restrict_chat_member(
            chat_id, uid, 
            ChatPermissions(can_send_messages=True, can_send_photos=True, can_send_other_messages=True)
        )
        await update.message.reply_text("🔊 Communication permissions restored.")
    except:
        await update.message.reply_text("❌ Action failed.")

# ---------------- FILTER INTEGRATION ----------------
async def set_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id if update.effective_chat.type != 'private' else context.user_data.get('current_chat_id')
    if not chat_id or not await check_admin(chat_id, update.effective_user.id, context.bot): return
    if len(context.args) < 2: return await update.message.reply_text("Usage: /filter <trigger> <reply text>")

    keyword = context.args[0].lower()
    reply = " ".join(context.args[1:])
    filters_db[(chat_id, keyword)] = reply
    await update.message.reply_text(f"✅ Auto filter established for trigger phrase '{keyword}'")

async def stop_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id if update.effective_chat.type != 'private' else context.user_data.get('current_chat_id')
    if not chat_id or not await check_admin(chat_id, update.effective_user.id, context.bot): return
    if not context.args: return await update.message.reply_text("Usage: /stop <trigger>")
    
    keyword = context.args[0].lower()
    key = (chat_id, keyword)
    if key in filters_db:
        del filters_db[key]
        await update.message.reply_text("❌ Auto filter terminated.")
    else:
        await update.message.reply_text("Trigger keyword profile not found.")

# ---------------- DYNAMIC BANNER SETUP (WELCOME/GOODBYE) ----------------
async def setwelcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id if update.effective_chat.type != 'private' else context.user_data.get('current_chat_id')
    if not chat_id or not await check_admin(chat_id, update.effective_user.id, context.bot): return
    text = " ".join(context.args)
    if not text: return await update.message.reply_text("Usage: /setwelcome <custom text>")
    welcome_db[chat_id] = text
    await update.message.reply_text("✅ Group welcome layout saved.")

async def welcome_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id if update.effective_chat.type != 'private' else context.user_data.get('current_chat_id')
    if not chat_id: return
    msg = welcome_db.get(chat_id, DEFAULT_WELCOME)
    await update.message.reply_text("📌 Active group welcome text:\n\n" + msg)

async def resetwelcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id if update.effective_chat.type != 'private' else context.user_data.get('current_chat_id')
    if not chat_id or not await check_admin(chat_id, update.effective_user.id, context.bot): return
    if chat_id in welcome_db: del welcome_db[chat_id]
    await update.message.reply_text("🔄 Welcome parameters restored to default defaults.")

async def setgoodbye(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id if update.effective_chat.type != 'private' else context.user_data.get('current_chat_id')
    if not chat_id or not await check_admin(chat_id, update.effective_user.id, context.bot): return
    text = " ".join(context.args)
    if not text: return await update.message.reply_text("Usage: /setgoodbye <custom text>")
    goodbye_db[chat_id] = text
    await update.message.reply_text("✅ Group goodbye layout saved.")

async def goodbye_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id if update.effective_chat.type != 'private' else context.user_data.get('current_chat_id')
    if not chat_id: return
    msg = goodbye_db.get(chat_id, DEFAULT_GOODBYE)
    await update.message.reply_text("📌 Active group goodbye text:\n\n" + msg)

async def resetgoodbye(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id if update.effective_chat.type != 'private' else context.user_data.get('current_chat_id')
    if not chat_id or not await check_admin(chat_id, update.effective_user.id, context.bot): return
    if chat_id in goodbye_db: del goodbye_db[chat_id]
    await update.message.reply_text("🔄 Goodbye parameters restored to default defaults.")

# ---------------- GLOBAL SERVICE EVENTS & SYSTEM MONITOR ----------------
async def user_join_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        chat = update.effective_chat
        msg = welcome_db.get(chat.id, DEFAULT_WELCOME)
        await context.bot.send_message(chat.id, format_text(msg, member, chat))

async def user_leave_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.left_chat_member:
        user = update.message.left_chat_member
        chat = update.effective_chat
        msg = goodbye_db.get(chat.id, DEFAULT_GOODBYE)
        await context.bot.send_message(chat.id, format_text(msg, user, chat))

async def global_message_scanner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    text = update.message.text.lower()
    chat_id = update.effective_chat.id
    user = update.message.from_user

    for (cid, keyword), reply in filters_db.items():
        if cid == chat_id and keyword in text:
            await update.message.reply_text(format_text(reply, user))

# ---------------- RUNTIME EXECUTION ----------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Base Architecture
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("connect", connect_cmd))
    app.add_handler(CallbackQueryHandler(button))

    # General User Services
    app.add_handler(CommandHandler("rules", rules_cmd))
    app.add_handler(CommandHandler("adminlist", adminlist_cmd))
    app.add_handler(CommandHandler("warn", warn_cmd))

    # Core Action Engines
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(CommandHandler("unmute", unmute))

    # Custom Response Configurations
    app.add_handler(CommandHandler("filter", set_filter))
    app.add_handler(CommandHandler("stop", stop_filter))

    # Notification Layout Management
    app.add_handler(CommandHandler("setwelcome", setwelcome))
    app.add_handler(CommandHandler("welcome", welcome_cmd))
    app.add_handler(CommandHandler("resetwelcome", resetwelcome))
    app.add_handler(CommandHandler("setgoodbye", setgoodbye))
    app.add_handler(CommandHandler("goodbye", goodbye_cmd))
    app.add_handler(CommandHandler("resetgoodbye", resetgoodbye))

    # Active Stream Event Mapping
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, user_join_event))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, user_leave_event))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, global_message_scanner))

    print("Bright Security Bot is running smoothly...")
    app.run_polling()

if __name__ == '__main__':
    main()
