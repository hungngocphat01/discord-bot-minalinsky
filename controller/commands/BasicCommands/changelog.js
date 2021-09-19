const { SlashCommandBuilder, codeBlock } = require('@discordjs/builders');
const fs = require('fs');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('changelog')
		.setDescription('Get the bot\'s changelog.'),
	async execute(interaction) {
		let changelog = fs.readFileSync('CHANGELOG').toString();
        changelog = (changelog.length >= 2000) 
            ? codeBlock(changelog.substr(0, 1970) + "\n...(truncated)")
            : changelog;
        await interaction.reply(changelog);
	},
};