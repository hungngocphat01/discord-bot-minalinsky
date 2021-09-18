const { SlashCommandBuilder, codeBlock } = require('@discordjs/builders');
const fs = require('fs');
const os = require('os');
const botintro = require('../../utils/botintro');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('status')
		.setDescription('Get the current status of the bot.'),
	async execute(interaction) {
		statusString = botintro.getHeader();
        statusString += `\nBot started at: ${global.botStatus["start_time"]}`;
        statusString += `\nRunning on Heroku: ${global.botStatus["on_heroku"]}`;
        statusString += `\nHost operating system: ${os.type()} ${os.release()}`;
        statusString += `\nCurrent server: ${interaction.guild.name}`;
        await interaction.reply(codeBlock(statusString));
	},
};