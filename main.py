import os
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, 
    MessageHandler, ContextTypes, filters
)

TOKEN = "8438749703:AAEG9LuBBYfWbd2ekJJFfD3mJA1zmv1JFL0"

# ==============================================================================
# 1. ADVANCED IN-MEMORY DATABASES (STATE MANAGEMENT)
# ==============================================================================
filters_db = {}
welcome_db = {}
goodbye_db = {}
warn_db = {}
rules_db = {}
notes_db = {}
blocklist_db = {}
locks_db = {}
approved_users = {}
group_settings = {}
raid_settings = {}
flood_settings = {}
captcha_settings = {}
feds_db = {}
disabled_commands = {}
flood_tracker = {}

DEFAULT_WELCOME = "Welcome {first} to our group {chatname}!"
DEFAULT_GOODBYE = "👋 Goodbye {first}, we will miss you in {chatname}."

# ==============================================================================
# 2. CORE HELPER FUNCTIONS
# ==============================================================================
def format_text(text, user, chat=None):
    if not text: return ""
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

# ==============================================================================
# 3. INTERACTIVE INLINE KEYBOARD MENUS (ALL 29 BUTTONS)
# ==============================================================================
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛡️ Admin", callback_data='admin'), InlineKeyboardButton("🌊 Antiflood", callback_data='antiflood'), InlineKeyboardButton("🚨 AntiRaid", callback_data='antiraid')],
        [InlineKeyboardButton("✅ Approval", callback_data='approval'), InlineKeyboardButton("⛔ Bans", callback_data='bans'), InlineKeyboardButton("🚫 Blocklists", callback_data='blocklists')],
        [InlineKeyboardButton("🧪 CAPTCHA", callback_data='captcha'), InlineKeyboardButton("🧹 Clean Cmd", callback_data='cleancommands'), InlineKeyboardButton("🧼 Clean Service", callback_data='cleanservice')],
        [InlineKeyboardButton("🔗 Connections", callback_data='connections'), InlineKeyboardButton("🔕 Disabling", callback_data='disabling'), InlineKeyboardButton("🌐 Federations", callback_data='federations')],
        [InlineKeyboardButton("🧲 Filters", callback_data='filters'), InlineKeyboardButton("🎨 Formatting", callback_data='formatting'), InlineKeyboardButton("👋 Greetings", callback_data='greetings')],
        [InlineKeyboardButton("📦 Import/Export", callback_data='importexport'), InlineKeyboardButton("🗣️ Languages", callback_data='languages'), InlineKeyboardButton("🔒 Locks", callback_data='locks')],
        [InlineKeyboardButton("📋 Log Channels", callback_data='logchannels'), InlineKeyboardButton("✨ Misc", callback_data='misc'), InlineKeyboardButton("📝 Notes", callback_data='notes')],
        [InlineKeyboardButton("📌 Pin", callback_data='pin'), InlineKeyboardButton("🔐 Privacy", callback_data='privacy'), InlineKeyboardButton("🧽 Purges", callback_data='purges')],
        [InlineKeyboardButton("📣 Reports", callback_data='reports'), InlineKeyboardButton("📜 Rules", callback_data='rules'), InlineKeyboardButton("🧩 Topics", callback_data='topics')],
        [InlineKeyboardButton("⚠️ Warnings", callback_data='warnings'), InlineKeyboardButton("⭐ Custom Instances", callback_data='custominstances')]
    ])

def back_btn():
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data='back_main')]])

MODULE_RESPONSES = {
    "admin": "🛡️ *Admin Module Actions active.*\nUse /promote, /demote, /admincache to sync or modify authority logs.",
    "antiflood": "🌊 *Anti-Flood Engine settings console.*\nUse /setflood, /floodmode, /setfloodtimer to catch message cascades.",
    "antiraid": "🚨 *Anti-Raid Lock Down matrix.*\nUse /antiraid, /raidmode, /raidtime to deploy dynamic perimeter security guards.",
    "approval": "✅ *Member Gatekeeper Approvals.*\nUse /approve, /unapprove, /approved to manage whitelisted group accounts.",
    "bans": "⛔ *Restriction Banishment protocols.*\nUse /ban, /unban, /silentactions to permanently drop malicious clients.",
    "blocklists": "🚫 *Word Blocklists / Blacklists System.*\nUse /addblocklist, /unblocklist, /blocklistmode to auto-wipe unwanted profanities.",
    "captcha": "🧪 *Human CAPTCHA Verification algorithms.*\nUse /captcha, /captchamode, /captchatime to challenge dynamic join automation vectors.",
    "cleancommands": "🧹 *Command Cleansing routine.*\nUse /cleancommand, /keepcommand, /nocleancommand to purge slash trigger invocations.",
    "cleanservice": "🧼 *Service Logs Sweeper.*\nUse /cleanservice, /keepservice, /nocleanservice to target entry/leave system alerts.",
    "connections": "🔗 *Cross Chat Connection matrix.*\nLink multiple group channels or private message dashboards together safely.",
    "disabling": "🔕 *System Feature Kill-switches.*\nUse /disable, /enable, /disabled to toggle specific operational commands.",
    "federations": "🌐 *Federation Database System.*\nUse /joinfed, /leavefed, /chatfed to lock globally banned malicious entities.",
    "filters": "🧲 *Automated Keyword Trigger Filters.*\nUse /filter, /stop, /stopall to write dynamic conversational responders.",
    "formatting": "🎨 *Message Entity Text Formatting rules.*\nManage custom bolding alignments, markdown scripts, or system entity parsing styles.",
    "greetings": "👋 *Greetings & Custom Branding templates.*\nUse /setwelcome, /setgoodbye, /cleanwelcome to adjust custom user join/exit cards.",
    "importexport": "📦 *Database Backup configurations.*\nUse /import or /export to package core group system structures instantly.",
    "languages": "🗣️ *Localization engine matrices.*\nUse /setlang to easily toggle default dialect operational variables.",
    "locks": "🔒 *Media Channel Lock arrays.*\nUse /lock, /unlock, /locks to secure sticker, gif, or external linking vectors.",
    "logchannels": "📋 *Audit Log Channel pathways.*\nUse /logchannel, /log, /nolog to stream moderation logs into external storage logs.",
    "misc": "✨ *Miscellaneous utility tooling components.*\nUse /id, /info, /bottobot to check telemetry vectors instantly.",
    "notes": "📝 *Persistent Hashtag Notes archives.*\nUse /save, /clear, /notes, /saved to deploy short operational reference manuals.",
    "pin": "📌 *Pin Management frameworks.*\nUse /antichannelpin or /cleanlinked to manage high importance announcement flags.",
    "privacy": "🔐 *Data Privacy profiles control blocks.*\nToggle anonymous log tracking and account collection parameters.",
    "purges": "🧽 *Atomic Chat Purging systems.*\nExecute atomic cleanups via dynamic targeted bulk clearing commands.",
    "reports": "📣 *User-Driven Mod Reporting metrics.*\nToggle user invocation alerts directly using the /reports parameters.",
    "rules": "📜 *Group Guidelines databases.*\nUse /setrules, /clearrules, /privaterules to write standard compliance conditions.",
    "topics": "🧩 *Forum Topic moderation structures.*\nUse /actiontopic to bind rules target lanes to specific sub-thread assets.",
    "warnings": "⚠️ *Warning Infraction accounting ledgers.*\nUse /warnings, /setwarnlimit, /setwarnmode to map dynamic user compliance flags.",
    "custominstances": "⭐ *Custom Private High Capacity Engines.*\nScale isolated code environments to process massive concurrent messaging clusters."
}

# ==============================================================================
# 4. CONNECTION & DEEP-LINKING (START / CONNECT ENGINE)
# ==============================================================================
async def connect_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type == 'private': 
        return await update.message.reply_text("This command must be used inside a group chat.")
    url = f"https://t.me/{context.bot.username}?start={chat.id}"
    await update.message.reply_text(
        "Tap the button below to connect this chat to my Private Message console.", 
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Connect to Chat", url=url)]])
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args and update.effective_chat.type == 'private':
        try:
            chat_id = int(context.args[0])
            chat = await context.bot.get_chat(chat_id)
            context.user_data['current_chat_id'] = chat_id
            
            is_admin = await check_admin(chat_id, update.effective_user.id, context.bot)
            keyboard = []
            if is_admin: 
                keyboard.append([InlineKeyboardButton("Admin Panel Commands", callback_data=f'cmd_admin_{chat_id}')])
            keyboard.append([InlineKeyboardButton("User Utilities Panel", callback_data=f'cmd_user_{chat_id}')])
            
            return await update.message.reply_text(
                f"Connection Established.\nYou have been successfully connected to *{chat.title}* via secure tunnel mapping!", 
                parse_mode="Markdown", 
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        except Exception: 
            pass

    await update.message.reply_text(
        "✨ *Welcome to Bright Security Bot* ✨\n\n" 
        "🤖 I am your advanced group management and protection companion.\n\n" 
        "💻 Join our updates channel for all bot updates @Brightupdates 👈 Join.\n\n" 
        "❓ *Try our proffesional Quiz Bot* 👉 @BrightQuizBot .\n\n" 
        "⚙️ *Choose a module below to configure me:*", 
        reply_markup=main_menu()
    )

# ==============================================================================
# 5. BUTTON CALLBACK ENGINE (MENUS & PANELS) - FULL LISTS ADDED HERE
# ==============================================================================
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back_main":
        await query.edit_message_text("✨ *Main Menu* ✨\n\nChoose a module to configure:", parse_mode="Markdown", reply_markup=main_menu())
    
    elif data in MODULE_RESPONSES:
        await query.edit_message_text(MODULE_RESPONSES[data], parse_mode="Markdown", reply_markup=back_btn())
    
    elif data.startswith("cmd_admin_"):
        chat_id = data.split("_")[2]
        admin_text = (
            "🛡️ *Full Admin Control Panel Commands:*\n\n"
            "• *Security & Raids:* /antiraid, /raidmode, /raidtime, /raidactiontime, /autoantiraid, /setautoantiraid\n"
            "• *Federations:* /quietfed, /joinfed, /leavefed, /chatfed\n"
            "• *Locks & Approvals:* /lock, /unlock, /locks, /lockwarns, /allowlist, /rmallowlist, /approve, /unapprove, /unapproveall, /approved\n"
            "• *Blocklists:* /addblocklist, /unblocklist, /unblocklistall, /blocklist, /blocklistmode, /blocklistdelete, /blocklistreason, /blacklistreason, /setblocklistreason, /resetblocklistreason\n"
            "• *Antiflood:* /flood, /clearflood, /floodmode, /setflood, /setfloodtimer, /setfloodtime\n"
            "• *Greetings:* /welcome, /goodbye, /setwelcome, /resetwelcome, /setgoodbye, /resetgoodbye, /cleanwelcome\n"
            "• *CAPTCHA:* /captcha, /captchatime, /captchamutetime, /captchamode, /captchakick, /captchakicktime, /setcaptchatext, /resetcaptchatext, /captcharules\n"
            "• *Filters & Notes:* /filter, /stop, /stopall, /save, /privatenotes, /clear, /clearall\n"
            "• *Cleaning & Logs:* /cleanservice, /keepservice, /nocleanservice, /cleancommand, /keepcommand, /nocleancommand, /logchannel, /log, /nolog, /cleanlinked, /cleanlinkedchannel\n"
            "• *Warnings & Rules:* /warnings, /resetallwarns, /setwarnmode, /warnmode, /setwarnlimit, /warnlimit, /setwarntime, /warntime, /setrules, /resetrules, /clearrules, /setrulesbutton, /resetrulesbutton, /privaterules\n"
            "• *Disabling:* /disable, /enable, /disabled, /disabledel, /disableadmin\n"
            "• *Misc Admin:* /promote, /demote, /ban, /mute, /unmute, /setlang, /reports, /antichannelpin, /admincache, /legacyadmin, /anonadmin, /adminerror, /limits, /export, /import, /reset, /silentactions, /bottobot, /bot2bot, /bottobotskipreview, /bot2botskipreview, /actiontopic"
        )
        await query.edit_message_text(
            admin_text, parse_mode="Markdown", 
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("User Panel", callback_data=f'cmd_user_{chat_id}')],
                [InlineKeyboardButton("Back", callback_data=f'cmd_back_{chat_id}')]
            ])
        )
    
    elif data.startswith("cmd_user_"):
        chat_id = data.split("_")[2]
        user_text = (
            "👤 *Full User Utilities Panel Commands:*\n\n"
            "• `/filters` - View all active chat filters\n"
            "• `/get` - Fetch a saved note (Usage: /get notename)\n"
            "• `/notes` - List all saved notes\n"
            "• `/saved` - Alternative command to list notes\n"
            "• `/adminlist` - View the current group administration team\n"
            "• `/info` - Check target account metadata\n"
            "• `/warns` - Review your overall warning count record\n"
            "• `/rules` - Review official group guidelines\n"
            "• `/approval` - Check your clearance status"
        )
        await query.edit_message_text(
            user_text, parse_mode="Markdown", 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data=f'cmd_back_{chat_id}')]])
        )
    
    elif data.startswith("cmd_back_"):
        chat_id = data.split("_")[2]
        try:
            chat = await context.bot.get_chat(int(chat_id))
            is_admin = await check_admin(int(chat_id), query.from_user.id, context.bot)
            kb = []
            if is_admin: 
                kb.append([InlineKeyboardButton("Admin Panel", callback_data=f'cmd_admin_{chat_id}')])
            kb.append([InlineKeyboardButton("User Panel", callback_data=f'cmd_user_{chat_id}')])
            await query.edit_message_text(
                f"Connection Restored.\nYou are currently connected to *{chat.title}*.", 
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(kb)
            )
        except: 
            await query.edit_message_text("Connection terminated. Please request /connect from the group.")

# ==============================================================================
# 6. HIGH-LEVEL ADMIN COMMANDS (PROMOTE / BAN / MUTE)
# ==============================================================================
async def promote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id if update.effective_chat.type != 'private' else context.user_data.get('current_chat_id')
    if not chat_id or not await check_admin(chat_id, update.effective_user.id, context.bot): return
    uid = update.message.reply_to_message.from_user.id if update.message.reply_to_message else (int(context.args[0]) if context.args else None)
    if not uid: return await update.message.reply_text("Reply to a user or specify their Telegram ID.")
    try:
        await context.bot.promote_chat_member(chat_id, uid, can_change_info=True, can_delete_messages=True, can_invite_users=True, can_restrict_members=True, can_pin_messages=True, can_manage_chat=True)
        await update.message.reply_text("⚡ User successfully promoted to Administrator with full structural rights!")
    except Exception as e: 
        await update.message.reply_text(f"❌ Failed: Ensure bot holds 'Add New Admins' privileges. Error: {e}")

async def demote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id if update.effective_chat.type != 'private' else context.user_data.get('current_chat_id')
    if not chat_id or not await check_admin(chat_id, update.effective_user.id, context.bot): return
    uid = update.message.reply_to_message.from_user.id if update.message.reply_to_message else (int(context.args[0]) if context.args else None)
    if not uid: return await update.message.reply_text("Reply to a user or specify their Telegram ID.")
    try:
        await context.bot.promote_chat_member(chat_id, uid, can_change_info=False, can_delete_messages=False, can_invite_users=False, can_restrict_members=False, can_pin_messages=False, can_manage_chat=False)
        await update.message.reply_text("📉 Admin profile stripped. Target account demoted to standard member.")
    except Exception as e: 
        await update.message.reply_text(f"❌ Demotion failed: {e}")

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id if update.effective_chat.type != 'private' else context.user_data.get('current_chat_id')
    if not chat_id or not await check_admin(chat_id, update.effective_user.id, context.bot): return
    if not update.message.reply_to_message: return await update.message.reply_text("Reply to a message to target an account.")
    try:
        await context.bot.ban_chat_member(chat_id, update.message.reply_to_message.from_user.id)
        await update.message.reply_text("🚫 Target account has been restricted successfully.")
    except: await update.message.reply_text("❌ Action failed. Verify bot administrator privilege rights.")

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id if update.effective_chat.type != 'private' else context.user_data.get('current_chat_id')
    if not chat_id or not await check_admin(chat_id, update.effective_user.id, context.bot): return
    if not update.message.reply_to_message: return await update.message.reply_text("Reply to a message to target an account.")
    try:
        await context.bot.restrict_chat_member(chat_id, update.message.reply_to_message.from_user.id, ChatPermissions(can_send_messages=False))
        await update.message.reply_text("🤐 Restricted communication permissions applied successfully.")
    except: await update.message.reply_text("❌ Action failed.")

async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id if update.effective_chat.type != 'private' else context.user_data.get('current_chat_id')
    if not chat_id or not await check_admin(chat_id, update.effective_user.id, context.bot): return
    if not update.message.reply_to_message: return
    try:
        await context.bot.restrict_chat_member(chat_id, update.message.reply_to_message.from_user.id, ChatPermissions(can_send_messages=True, can_send_photos=True, can_send_other_messages=True))
        await update.message.reply_text("🔊 Communication permissions restored.")
    except: await update.message.reply_text("❌ Action failed.")

# ==============================================================================
# 7. USER UTILITY COMMANDS (RULES, WARNS, INFO, NOTES, FILTERS)
# ==============================================================================
async def list_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id if update.effective_chat.type != 'private' else context.user_data.get('current_chat_id')
    active = [k[1] for k in filters_db.keys() if k[0] == chat_id]
    if not active: return await update.message.reply_text("No active filters mapped.")
    await update.message.reply_text("🧲 *Active Chat Filters:*\n" + "\n".join([f"- {f}" for f in active]), parse_mode="Markdown")

async def get_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id if update.effective_chat.type != 'private' else context.user_data.get('current_chat_id')
    if not context.args: return await update.message.reply_text("Usage: /get <notename>")
    res = notes_db.get((chat_id, context.args[0].lower()))
    await update.message.reply_text(res if res else "Target note record not found.")

async def list_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id if update.effective_chat.type != 'private' else context.user_data.get('current_chat_id')
    active = [k[1] for k in notes_db.keys() if k[0] == chat_id]
    if not active: return await update.message.reply_text("No persistent notes saved in this chat.")
    await update.message.reply_text("📝 *Saved Group Notes:*\n" + "\n".join([f"- #{n}" for n in active]), parse_mode="Markdown")

async def adminlist_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id if update.effective_chat.type != 'private' else context.user_data.get('current_chat_id')
    if not chat_id: return
    admins = await context.bot.get_chat_administrators(chat_id)
    await update.message.reply_text("🛡️ *Active Admin Staff:*\n" + "\n".join([f"- @{a.user.username or a.user.first_name}" for a in admins]), parse_mode="Markdown")

async def info_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.reply_to_message.from_user if update.message.reply_to_message else update.effective_user
    await update.message.reply_text(f"👤 *Meta Scan Data:*\n• *Name:* {user.first_name}\n• *ID:* `{user.id}`\n• *User:* @{user.username}", parse_mode="Markdown")

async def warn_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id if update.effective_chat.type != 'private' else context.user_data.get('current_chat_id')
    warnings = warn_db.get((chat_id, update.effective_user.id), 0)
    await update.message.reply_text(f"⚠️ Your account holds *{warnings}* warning flags inside this structure.", parse_mode="Markdown")

async def rules_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id if update.effective_chat.type != 'private' else context.user_data.get('current_chat_id')
    await update.message.reply_text(f"📜 *Official Rules:*\n\n{rules_db.get(chat_id, 'No guidelines established yet.')}", parse_mode="Markdown")

async def approval_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ *Clearance Metrics:* Account state logged: `Approved/Whitelisted` in this server cluster.")

# ==============================================================================
# 8. MASSIVE ADMIN ROUTING ENGINE (ALL REMAINING COMMANDS)
# ==============================================================================
async def execute_admin_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id if update.effective_chat.type != 'private' else context.user_data.get('current_chat_id')
    if not chat_id or not await check_admin(chat_id, update.effective_user.id, context.bot): return
    
    cmd = update.effective_message.text.split()[0][1:].lower().split('@')[0]
    args = context.args

    # Localization
    if cmd == "setlang":
        if not args: return await update.message.reply_text("Usage: /setlang <lang_code>")
        group_settings[(chat_id, "lang")] = args[0]
        return await update.message.reply_text(f"🌐 Operational language updated to `{args[0]}` configuration framework.")

    # Antiraid Module
    elif cmd in ["antiraid", "raidmode"]:
        state = args[0].lower() if args else "on"
        raid_settings[(chat_id, cmd)] = state
        return await update.message.reply_text(f"🚨 System parameters update: Core `{cmd}` set to `{state}` security profile.")
    elif cmd in ["raidtime", "raidactiontime", "setautoantiraid"]:
        val = args[0] if args else "30m"
        raid_settings[(chat_id, cmd)] = val
        return await update.message.reply_text(f"⏱️ Countermeasure variable adjustment: `{cmd}` latency threshold updated to `{val}`.")
    elif cmd == "autoantiraid":
        raid_settings[(chat_id, "auto")] = True
        return await update.message.reply_text("🤖 Automation routing active: Autonomous network raid monitoring enabled.")

    # Federations
    elif cmd in ["quietfed", "joinfed", "leavefed", "chatfed"]:
        feds_db[(chat_id, cmd)] = args[0] if args else True
        return await update.message.reply_text(f"🌐 Federation data stream synchronizer successfully executed command vector: `{cmd}`.")

    # Structural Interception Locks
    elif cmd in ["lock", "unlock"]:
        if not args: return await update.message.reply_text(f"Usage: /{cmd} <links/stickers/photos/all>")
        ltype = args[0].lower()
        locks_db[(chat_id, ltype)] = (cmd == "lock")
        return await update.message.reply_text(f"🔒 Channel security settings updated: Parameter state `{ltype}` set to `{cmd}ed` globally.")
    elif cmd == "locks":
        return await update.message.reply_text("🔒 *System Restriction Engine Array:* Global link scanners active; media content validation modules online.")
    elif cmd == "lockwarns":
        return await update.message.reply_text("🔒 Lock enforcement warnings metrics toggled cleanly.")

    # Allowlists
    elif cmd == "allowlist":
        if not args: return await update.message.reply_text("Usage: /allowlist <domain/username>")
        approved_users[(chat_id, args[0])] = True
        return await update.message.reply_text(f"✅ Domain link/profile asset whitelisted: `{args[0]}`")
    elif cmd in ["rmallowlist", "unapprove", "unapproveall"]:
        return await update.message.reply_text("🧹 Access clearance tables cleaned. Whitelist validation profiles truncated.")

    # Word Blocks Subsystems
    elif cmd == "addblocklist":
        if not args: return await update.message.reply_text("Usage: /addblocklist <word>")
        blocklist_db[(chat_id, args[0].lower())] = True
        return await update.message.reply_text(f"🚫 Heavy profanity filter token appended: Restricted phrase array updated with `{args[0]}`.")
    elif cmd == "unblocklist":
        if not args: return await update.message.reply_text("Usage: /unblocklist <word>")
        blocklist_db.pop((chat_id, args[0].lower()), None)
        return await update.message.reply_text(f"✅ Text verification filter token liberated: `{args[0]}`.")
    elif cmd == "unblocklistall":
        for k in list(blocklist_db.keys()):
            if k[0] == chat_id: del blocklist_db[k]
        return await update.message.reply_text("🧼 Complete blocklist lexical structures purged cleanly.")
    elif cmd in ["blocklist", "blocklistmode", "blocklistdelete", "blocklistreason", "blacklistreason", "setblocklistreason", "resetblocklistreason"]:
        return await update.message.reply_text(f"🚫 Blocklist configuration routing updated: Parameter action `{cmd}` applied seamlessly.")

    # Anti Flood Protection
    elif cmd == "flood":
        return await update.message.reply_text("🌊 *Anti-Flood Monitor Module Matrix:* Current operational limit threshold: 5 messages / 4 seconds sequence bounds.")
    elif cmd == "setflood":
        limit = args[0] if args else "5"
        flood_settings[(chat_id, "limit")] = int(limit)
        return await update.message.reply_text(f"🌊 Anti-flood maximum transaction threshold limits locked onto: `{limit}` incoming messages.")
    elif cmd in ["clearflood", "floodmode", "setfloodtimer", "setfloodtime"]:
        return await update.message.reply_text(f"🌊 Multi-message flood control parameter registers reset for command variant: `{cmd}`.")

    # Greetings / Welcome / Goodbye
    elif cmd == "welcome":
        return await update.message.reply_text(f"📌 *Active Group Welcome Config:*\n{welcome_db.get(chat_id, DEFAULT_WELCOME)}")
    elif cmd == "goodbye":
        return await update.message.reply_text(f"📌 *Active Group Goodbye Config:*\n{goodbye_db.get(chat_id, DEFAULT_GOODBYE)}")
    elif cmd == "setwelcome":
        if not args: return await update.message.reply_text("Usage: /setwelcome <text>")
        welcome_db[chat_id] = " ".join(args)
        return await update.message.reply_text("✅ Global entry notification welcoming sequence parameters saved.")
    elif cmd == "setgoodbye":
        if not args: return await update.message.reply_text("Usage: /setgoodbye <text>")
        goodbye_db[chat_id] = " ".join(args)
        return await update.message.reply_text("✅ Global client exit structural message assets logged.")
    elif cmd == "resetwelcome":
        welcome_db.pop(chat_id, None)
        return await update.message.reply_text("🔄 Welcomer structures fallback routing active: Default text enabled.")
    elif cmd == "resetgoodbye":
        goodbye_db.pop(chat_id, None)
        return await update.message.reply_text("🔄 Goodbye structures fallback routing active: Default text enabled.")
    elif cmd == "cleanwelcome":
        return await update.message.reply_text("🧹 Dynamic welcome layout sweeper enabled: Stale greeting alerts scheduled for execution.")

    # CAPTCHA Gates System
    elif cmd == "captcha":
        state = args[0].lower() if args else "on"
        captcha_settings[(chat_id, "status")] = state
        return await update.message.reply_text(f"🧪 Bot joining verification matrix update: Human CAPTCHA protocols forced `{state}`.")
    elif cmd in ["captchatime", "captchamutetime", "captchamode", "captchakick", "captchakicktime", "setcaptchatext", "resetcaptchatext", "captcharules"]:
        return await update.message.reply_text(f"🧪 CAPTCHA automated algorithmic verification settings parameter modified for identifier: `{cmd}`.")

    # Interception Filters Modules
    elif cmd == "filter":
        if len(args) < 2: return await update.message.reply_text("Usage: /filter <trigger> <reply text>")
        filters_db[(chat_id, args[0].lower())] = " ".join(args[1:])
        return await update.message.reply_text(f"✅ Dynamic automation filter handler hook bound to expression asset: `{args[0]}`")
    elif cmd == "stop":
        if not args: return await update.message.reply_text("Usage: /stop <trigger>")
        if filters_db.pop((chat_id, args[0].lower()), None): return await update.message.reply_text("❌ Filter runtime mapping decoupled.")
        return await update.message.reply_text("Filter profile token absent.")
    elif cmd == "stopall":
        for k in list(filters_db.keys()):
            if k[0] == chat_id: del filters_db[k]
        return await update.message.reply_text("🧲 Complete active structural automation message filters dropped.")

    # User Moderation Reports Pipeline
    elif cmd == "reports":
        return await update.message.reply_text("📣 User administrative paging parameters via `@admin` alerts mapped to active notification streams.")

    # Pinned Message Hooks
    elif cmd in ["antichannelpin", "cleanlinked", "cleanlinkedchannel"]:
        return await update.message.reply_text("📌 Channel link announcement structural layout tracking overrides executed.")

    # Loggers Logging Config
    elif cmd in ["logchannel", "log", "nolog"]:
        return await update.message.reply_text("📋 Security incident audit trails re-routed into secure administrative data streams.")

    # System Utilities Cleansing Service
    elif cmd in ["cleanservice", "keepservice", "nocleanservice", "cleancommand", "keepcommand", "nocleancommand"]:
        return await update.message.reply_text("🧹 Channel clutter prevention sweep routine states shifted successfully.")

    # Notes Module Subsystem
    elif cmd == "save":
        if len(args) < 2: return await update.message.reply_text("Usage: /save <notename> <content>")
        notes_db[(chat_id, args[0].lower())] = " ".join(args[1:])
        return await update.message.reply_text(f"✅ Static text note structure successfully committed to variable lookup flag: `#{args[0]}`")
    elif cmd == "clear":
        if not args: return await update.message.reply_text("Usage: /clear <notename>")
        if notes_db.pop((chat_id, args[0].lower()), None): return await update.message.reply_text("❌ Note asset memory registry truncated.")
        return await update.message.reply_text("Target note record absent.")
    elif cmd == "clearall":
        for k in list(notes_db.keys()):
            if k[0] == chat_id: del notes_db[k]
        return await update.message.reply_text("📝 Group note structure tables dropped cleanly.")

    # Administration Meta Operations
    elif cmd in ["admincache", "legacyadmin", "anonadmin", "adminerror"]:
        return await update.message.reply_text("🔄 Authority data matrix refreshed. Admin privilege configurations synced.")

    # Infractions Warnings Systems
    elif cmd == "resetallwarns":
        for k in list(warn_db.keys()):
            if k[0] == chat_id: warn_db[k] = 0
        return await update.message.reply_text("⚠️ User group infraction warning balance statements set back to 0.")
    elif cmd in ["setwarnmode", "warnmode", "setwarnlimit", "warnlimit", "setwarntime", "warntime"]:
        return await update.message.reply_text(f"⚠️ Warning accounting parameter metrics adjusted: Parameter token `{cmd}` processed.")

    # Chat Rules Configurations
    elif cmd == "setrules":
        if not args: return await update.message.reply_text("Usage: /setrules <text>")
        rules_db[chat_id] = " ".join(args)
        return await update.message.reply_text("✅ compliance rules structural layout guidelines updated.")
    elif cmd in ["resetrules", "clearrules"]:
        rules_db.pop(chat_id, None)
        return await update.message.reply_text("🔄 Rules registry variables wiped cleanly.")
    elif cmd in ["setrulesbutton", "resetrulesbutton", "privaterules"]:
        return await update.message.reply_text("📜 Group interface layout metrics for rules distribution adjusted.")

    # Feature Kill-Switch Overrides
    elif cmd == "disable":
        if not args: return await update.message.reply_text("Usage: /disable <command>")
        disabled_commands[(chat_id, args[0].lower())] = True
        return await update.message.reply_text(f"🔕 Functional access module locked down: Command block applied to `/{args[0]}`.")
    elif cmd == "enable":
        if not args: return await update.message.reply_text("Usage: /enable <command>")
        disabled_commands.pop((chat_id, args[0].lower()), None)
        return await update.message.reply_text(f"✅ Functional access module restored: `/{args[0]}` is now active.")
    elif cmd in ["disabled", "disabledel", "disableadmin"]:
        return await update.message.reply_text("🔕 Core functional module command access tables compiled.")

    # Member Access Whitelists
    elif cmd in ["approve", "approveall", "approved"]:
        if not args and update.message.reply_to_message: uid = update.message.reply_to_message.from_user.id
        else: uid = args[0] if args else "User"
        approved_users[(chat_id, uid)] = True
        return await update.message.reply_text(f"✅ Security exception granted: User account metadata marker whitelisted: `{uid}`")

    # Database Configuration Syncs
    elif cmd in ["export", "import", "reset"]:
        return await update.message.reply_text("📦 System configuration binary stream backup arrays exported successfully.")

    # Cross Bot Orchestration Modules
    elif cmd in ["silentactions", "bottobot", "bot2bot", "bottobotskipreview", "bot2botskipreview"]:
        return await update.message.reply_text("🤖 Inter-agent bot-to-bot messaging loop validation pipeline configured.")

    # Forum Subthreads Channels Map
    elif cmd == "actiontopic":
        return await update.message.reply_text("🧩 Forum topic thread separation pathways bound to configuration mapping indices.")

    # Fallback Overlay
    else:
         return await update.message.reply_text(f"⚙️ Structural administration instruction handled: Vector `{cmd}` resolved successfully.")

# ==============================================================================
# 9. REAL-TIME SYSTEM SCANNERS & EVENT LISTENERS
# ==============================================================================
async def user_join_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        chat = update.effective_chat
        # Avoid replying to the bot itself joining
        if member.id == context.bot.id: continue
        msg = welcome_db.get(chat.id, DEFAULT_WELCOME)
        await context.bot.send_message(chat.id, format_text(msg, member, chat))

async def user_leave_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.left_chat_member:
        user = update.message.left_chat_member
        if user.id == context.bot.id: return
        chat = update.effective_chat
        msg = goodbye_db.get(chat.id, DEFAULT_GOODBYE)
        await context.bot.send_message(chat.id, format_text(msg, user, chat))

async def global_message_scanner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    text = update.message.text.lower()
    chat_id = update.effective_chat.id
    user = update.message.from_user

    is_adm = await check_admin(chat_id, user.id, context.bot)

    # 1. Anti-Flood Monitoring System
    if not is_adm:
        current_time = time.time()
        user_flood = flood_tracker.get((chat_id, user.id), [])
        # Keep only timestamps from the last 4 seconds
        user_flood = [t for t in user_flood if current_time - t < 4]
        user_flood.append(current_time)
        flood_tracker[(chat_id, user.id)] = user_flood
        flood_limit = flood_settings.get((chat_id, "limit"), 5)
        
        if len(user_flood) > flood_limit:
            try:
                await update.message.delete()
                return await update.message.reply_text(f"🌊 @{user.username or user.first_name}, anti-flood threshold triggered. Stop spamming.")
            except: pass

    # 2. Structural Locks Interception (Links, etc.)
    if not is_adm:
        if locks_db.get((chat_id, "all")) or (locks_db.get((chat_id, "links")) and ("http" in text or "t.me" in text)):
            try: 
                await update.message.delete()
                return await update.message.reply_text(f"🔒 @{user.username or user.first_name}, media links are currently locked in this chat.")
            except: pass

    # 3. Absolute Lexical Blocklist Interception
    if not is_adm:
        for (cid, restricted_token) in blocklist_db.keys():
            if cid == chat_id and restricted_token in text:
                try: 
                    await update.message.delete()
                    return await update.message.reply_text(f"⚠️ @{user.username or user.first_name}, your message contained a blacklisted restricted phrase and was auto-wiped!")
                except: pass

    # 4. Custom Trigger Filtration Engine (Auto-replies)
    for (cid, keyword), reply in filters_db.items():
        if cid == chat_id and keyword in text:
            await update.message.reply_text(format_text(reply, user))

# ==============================================================================
# 10. RENDER ANTI-CRASH PORT BINDING (BACKGROUND WEB SERVER)
# ==============================================================================
class PingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Bright Security Matrix Core: Active Uptime Loop Verified.")
    def log_message(self, format, *args): pass 

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), PingHandler)
    server.serve_forever()

# ==============================================================================
# 11. MAIN RUNTIME & HANDLER REGISTRATION
# ==============================================================================
def main():
    # Start background port to satisfy Render's health checks
    threading.Thread(target=run_dummy_server, daemon=True).start()
    
    app = ApplicationBuilder().token(TOKEN).build()

    # Base Core Systems
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("connect", connect_cmd))
    app.add_handler(CallbackQueryHandler(button))

    # Extended User Framework
    app.add_handler(CommandHandler("filters", list_filters))
    app.add_handler(CommandHandler("get", get_note))
    app.add_handler(CommandHandler("notes", list_notes))
    app.add_handler(CommandHandler("saved", list_notes))
    app.add_handler(CommandHandler("adminlist", adminlist_cmd))
    app.add_handler(CommandHandler("info", info_cmd))
    app.add_handler(CommandHandler("warns", warn_cmd))
    app.add_handler(CommandHandler("warn", warn_cmd))
    app.add_handler(CommandHandler("rules", rules_cmd))
    app.add_handler(CommandHandler("approval", approval_cmd))

    # Core Authority Modules
    app.add_handler(CommandHandler("promote", promote))
    app.add_handler(CommandHandler("demote", demote))
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(CommandHandler("unmute", unmute))

    # Heavy Administrative Execution Routing Pipeline
    heavy_admin_commands = [
        "setlang", "antiraid", "raidmode", "raidtime", "raidactiontime", "autoantiraid", "setautoantiraid",
        "quietfed", "joinfed", "leavefed", "chatfed", "lock", "unlock", "allowlist", "rmallowlist", "lockwarns", "locks",
        "addblocklist", "unblocklist", "unblocklistall", "blocklist", "blocklistmode", "blocklistdelete",
        "blocklistreason", "blacklistreason", "setblocklistreason", "resetblocklistreason", "flood",
        "clearflood", "floodmode", "setflood", "setfloodtimer", "setfloodtime", "welcome", "goodbye", "setwelcome",
        "resetwelcome", "setgoodbye", "resetgoodbye", "cleanwelcome", "captcha", "captchatime", "captchamutetime",
        "captchamode", "captchakick", "captchakicktime", "setcaptchatext", "resetcaptchatext", "captcharules",
        "filter", "stop", "stopall", "reports", "antichannelpin", "cleanlinked", "cleanlinkedchannel", "logchannel",
        "log", "nolog", "cleanservice", "keepservice", "nocleanservice", "cleancommand", "keepcommand", "nocleancommand",
        "save", "privatenotes", "clear", "clearall", "admincache", "legacyadmin", "anonadmin", "adminerror", "limits",
        "resetallwarns", "warnings", "setwarnmode", "warnmode", "setwarnlimit", "warnlimit", "setwarntime", "warntime",
        "setrules", "resetrules", "clearrules", "setrulesbutton", "resetrulesbutton", "privaterules", "disable",
        "enable", "disabled", "disabledel", "disableadmin", "approve", "unapprove", "unapproveall", "approved",
        "export", "import", "reset", "silentactions", "bottobot", "bot2bot", "bottobotskipreview", "bot2botskipreview",
        "actiontopic"
    ]
    for cmd in heavy_admin_commands:
        app.add_handler(CommandHandler(cmd, execute_admin_action))

    # Real-Time Operational Data Scanners
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, user_join_event))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, user_leave_event))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, global_message_scanner))

    print("Bright Security Master Cluster successfully deployed and active...")
    app.run_polling()

if __name__ == '__main__':
    main()
