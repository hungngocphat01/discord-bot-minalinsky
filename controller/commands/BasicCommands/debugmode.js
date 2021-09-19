const { SlashCommandBuilder, codeBlock } = require('@discordjs/builders');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('debugmode')
		.setDescription('Temporarily ignore all signals from discord')
        .addBooleanOption(
            o => o.setName('value').setDescription('true = debug mode on').setRequired(true)
        ),
	async execute(interaction) {
        const debugmode = interaction.options.getBoolean('value');
        global.botStatus.debug_mode = debugmode;

        await interaction.reply(codeBlock(`Debug mode toggled: ${debugmode}`));
	},
};