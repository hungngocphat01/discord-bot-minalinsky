const { SlashCommandBuilder, codeBlock } = require('@discordjs/builders');
const Event = require('../../../model/events');
const Generator = require('../../../view/notification-generator');
const thumbnailGetter = require('../../utils/event-thumbnail-getter');


module.exports = {
	data: new SlashCommandBuilder()
		.setName('nextev')
		.setDescription('Get next Love Live! event(s)'),
	async execute(interaction) {
        const nextEvents = await Event.fetchNextEvents(true);
        const embeds = await Generator.generateNotifEmbeds(nextEvents);
        await interaction.reply({ embeds: embeds });

		// Add picture
		for (const [index, row] of nextEvents.entries()) {
			var thumbnailUrl = await thumbnailGetter(row);
			embeds[index].setImage(thumbnailUrl);
		}
        await interaction.editReply({ embeds: embeds });
	},
};