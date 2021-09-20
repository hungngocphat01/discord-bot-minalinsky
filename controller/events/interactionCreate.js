const { codeBlock } = require('@discordjs/builders');
const MaintainerNotifier = require('../utils/notify-err-maintainer');

function parseInteractionArgs(interaction) {
	const options = interaction.options._hoistedOptions;
	return options.map(o => `${o.name}=${o.value}`).join('; ');
}

module.exports = {
	name: 'interactionCreate',
	async execute(interaction) {
		// Only process commands
		if (!interaction.isCommand()) return;
		logger(`${interaction.user.tag} in #${interaction.channel.name} called ${interaction.commandName} with args:`, parseInteractionArgs(interaction));
		
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
			const message = `Something went wrong when executing your command:\n ${codeBlock(e.stack)}`;
			try {
				await interaction.reply(message);
			} catch (e2) {
				await interaction.editReply(message);
			}
			await MaintainerNotifier(interaction.client, '');
		}
	},
};