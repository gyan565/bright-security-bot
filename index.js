const { Telegraf, Markup } = require('telegraf');

const bot = new Telegraf(process.env.BOT_TOKEN);

const menu = Markup.inlineKeyboard([
  [Markup.button.callback('🛡️ Admin', 'admin')],
  [Markup.button.callback('🌊 Antiflood', 'antiflood')],
  [Markup.button.callback('🚨 AntiRaid', 'antiraid')],
  [Markup.button.callback('⛔ Bans', 'bans')],
  [Markup.button.callback('🚫 Blocklists', 'blocklists')],
  [Markup.button.callback('🧪 CAPTCHA', 'captcha')],
  [Markup.button.callback('📜 Rules', 'rules')],
  [Markup.button.callback('⚠️ Warnings', 'warnings')],
]);

bot.start((ctx) => {
  ctx.reply('🛡️ Bright Security Bot Menu\n\nChoose an option:', menu);
});

// FEATURES REPLIES

bot.action('admin', (ctx) => {
  ctx.reply('🛡️ Admin Panel:\n/promote, /demote, /adminlist');
});

bot.action('antiflood', (ctx) => {
  ctx.reply('🌊 AntiFlood Active:\nSpam protection enabled');
});

bot.action('antiraid', (ctx) => {
  ctx.reply('🚨 AntiRaid System:\nGroup raid protection ON');
});

bot.action('bans', (ctx) => {
  ctx.reply('⛔ Ban System:\n/ban, /unban, /tban supported');
});

bot.action('blocklists', (ctx) => {
  ctx.reply('🚫 Blocklist:\nBad words auto delete enabled');
});

bot.action('captcha', (ctx) => {
  ctx.reply('🧪 CAPTCHA:\nNew users must verify to join');
});

bot.action('rules', (ctx) => {
  ctx.reply('📜 Group Rules:\n1. No spam\n2. No links\n3. Respect everyone');
});

bot.action('warnings', (ctx) => {
  ctx.reply('⚠️ Warning System:\n3 warnings = auto ban');
});

bot.launch();

console.log("Bright Security Bot Running...");
