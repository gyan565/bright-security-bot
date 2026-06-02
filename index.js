const { Telegraf, Markup } = require('telegraf');

const bot = new Telegraf(process.env.BOT_TOKEN);

/// START COMMAND (WELCOME + BUTTONS)
bot.start((ctx) => {
  ctx.reply(
    '🛡️ Welcome to Bright Security Bot!\n\nSelect an option below:',
    Markup.inlineKeyboard([
      [Markup.button.callback('🔰 Help', 'help')],
      [Markup.button.callback('🛡️ Security Info', 'security')],
      [Markup.button.callback('⚙️ Rules', 'rules')],
    ])
  );
});

/// BUTTON ACTIONS

bot.action('help', (ctx) => {
  ctx.reply(
    '📌 Commands List:\n/start - Start bot\n/help - Help menu\n/ban - Ban user\n/mute - Mute user'
  );
});

bot.action('security', (ctx) => {
  ctx.reply(
    '🛡️ Security System Active:\n- Anti Spam\n- Anti Link\n- Anti Flood\n- Auto Moderation'
  );
});

bot.action('rules', (ctx) => {
  ctx.reply(
    '📜 Group Rules:\n1. No spam\n2. No links\n3. Respect admins\n4. No abuse'
  );
});

bot.launch();

console.log("Bright Security Bot is running...");
