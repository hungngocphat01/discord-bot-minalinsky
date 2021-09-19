const { SlashCommandBuilder, codeBlock } = require('@discordjs/builders');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('purge')
		.setDescription('Delete large quantity of messages')
        .setDefaultPermission(false)
        .addIntegerOption(
            o => o.setName('num').setDescription('Number of messages to delete').setRequired(true)
        ),
	async execute(interaction) {
        const channel = interaction.channel;
        const num = interaction.options.getInteger('num');
        if (num >= 100) {
            await interaction.reply(codeBlock('You cannot delete more than 100 messages at once.'));
        }
        else {
            await channel.bulkDelete(num);
            await interaction.reply(codeBlock(`Successfully deleted ${num} messages.`));
        }
	},
    permissions: [
        {
            id: global.botConfig['server-owner-id'], // My ID
            type: 2, // 2: USER, 1: ROLE
            permission: true
        }
    ],
};