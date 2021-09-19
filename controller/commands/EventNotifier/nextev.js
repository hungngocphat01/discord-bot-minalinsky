const { SlashCommandBuilder, codeBlock } = require('@discordjs/builders');
const Event = require('../../../model/events');
const Generator = require('../../../view/notification-generator');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('nextev')
		.setDescription('Get next Love Live! event(s)'),
	async execute(interaction) {
        const nextEvents = await Event.fetchNextEvents();
        const embeds = Generator.generateNotifEmbeds(nextEvents);
        await interaction.reply({ embeds: embeds });
	},
};