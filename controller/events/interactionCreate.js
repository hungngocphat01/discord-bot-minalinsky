const { codeBlock } = require('@discordjs/builders');

module.exports = {
	name: 'interactionCreate',
	async execute(interaction) {
		if (!interaction.isCommand()) return;
		console.log(`${interaction.user.tag} in #${interaction.channel.name} called command: ${interaction.commandName}`);

		const command = interaction.client.commands.get(interaction.commandName);
		if (!command) return;

		try {
			await command.execute(interaction);
		} catch (e) {
			console.error(e);
			await interaction.reply(`Something went wrong when executing your command:\n ${codeBlock(e)}`);
		}
	},
};