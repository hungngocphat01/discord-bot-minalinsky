const { SlashCommandBuilder, codeBlock } = require('@discordjs/builders');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('debugmode')
		.setDescription('Temporarily ignore all signals from discord')
        .setDefaultPermission(false)
        .addBooleanOption(
            o => o.setName('value').setDescription('true = debug mode on').setRequired(true)
        ),
	async execute(interaction) {
        if (process.env.RUNNING_ON_HEROKU != 1) {
            logger(`Debug mode toggled but not running on Heroku`);
            return;
        }
        const debugmode = interaction.options.getBoolean('value');
        global.botStatus.debug_mode = debugmode;

        await interaction.reply(codeBlock(`Debug mode toggled: ${debugmode}`));
	},
    permissions: [
        {
            id: global.botConfig['server-owner-id'], // My ID
            type: 2, // 2: USER, 1: ROLE
            permission: true
        }
    ],
};