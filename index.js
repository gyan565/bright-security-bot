bot.start((ctx) => {
  ctx.reply(
    "🌹 Hey! I'm Bright Security Bot\n\nI help you manage and protect your group with smart security tools.",
    Markup.inlineKeyboard([
      [Markup.button.callback('🛡️ Admin', 'admin'), Markup.button.callback('🌊 Antiflood', 'antiflood'), Markup.button.callback('🚨 AntiRaid', 'antiraid')],
      [Markup.button.callback('⛔ Bans', 'bans'), Markup.button.callback('🚫 Blocklists', 'blocklists'), Markup.button.callback('🧪 CAPTCHA', 'captcha')],
      [Markup.button.callback('📜 Rules', 'rules'), Markup.button.callback('📣 Reports', 'reports'), Markup.button.callback('📋 Log Channels', 'logchannels')],
      [Markup.button.callback('🧹 Clean Commands', 'cleancommands'), Markup.button.callback('🧼 Clean Service', 'cleanservice'), Markup.button.callback('🔗 Connections', 'connections')],
      [Markup.button.callback('🔒 Locks', 'locks'), Markup.button.callback('👋 Greetings', 'greetings'), Markup.button.callback('🧲 Filters', 'filters')],
      [Markup.button.callback('🔕 Disabling', 'disabling'), Markup.button.callback('🗣️ Languages', 'languages'), Markup.button.callback('📦 Import/Export', 'importexport')],
      [Markup.button.callback('⚠️ Warnings', 'warnings'), Markup.button.callback('⭐ Custom Instances', 'custominstances')]
    ])
  );
});
