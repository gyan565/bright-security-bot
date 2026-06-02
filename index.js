const { Telegraf } = require('telegraf');

const bot = new Telegraf(process.env.BOT_TOKEN);

bot.start((ctx) => {
  ctx.reply(
    '🛡️ Welcome to Bright Security Bot!\n\nYour group protection system is now active.'
  );
});

bot.launch();

console.log('Bright Security Bot is running...');
