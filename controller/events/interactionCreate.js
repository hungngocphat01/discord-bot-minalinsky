const { codeBlock } = require('@discordjs/builders');

module.exports = {
	name: 'interactionCreate',
	async execute(interaction) {
		// Only process commands
		if (!interaction.isCommand()) return;
		logger(`${interaction.user.tag} in #${interaction.channel.name} called command: ${interaction.commandName}`);
		
		// Ignore if bot is in debug mode
		if (global.botStatus.debug_mode == true && interaction.commandName != 'debugmode') {
			logger(`Bot is in debug mode. Ignoring command.`);
			return;
		}
		
		// Fetch command
		const command = interaction.client.commands.get(interaction.commandName);
		if (!command) return;

		// Execute command
		try {
			await command.execute(interaction);
		} catch (e) {
			logger(e.stack);
			await interaction.reply(`Something went wrong when executing your command:\n ${codeBlock(e.stack)}`);
		}
	},
};