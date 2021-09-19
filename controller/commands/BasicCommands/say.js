const { SlashCommandBuilder, codeBlock } = require('@discordjs/builders');
const fs = require('fs');
const os = require('os');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('say')
		.setDescription('Echo a string')
        .addStringOption(
            o => o.setName('str').setDescription('String to echo').setRequired(true)
        ),
	async execute(interaction) {
        await interaction.reply(interaction.options.getString('str'));
	},
};