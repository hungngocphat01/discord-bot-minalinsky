const { SlashCommandBuilder, codeBlock } = require('@discordjs/builders');
const Event = require('../../../model/events');
const Generator = require('../../../view/notification-generator');
const thumbnailGetter = require('../../utils/event-thumbnail-getter');
const TableGenerator = require('../../../view/generate-events-table');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('event')
		.setDescription('Get next Love Live! event(s)')
		.addSubcommand(subcommand =>
			subcommand.setName('next').setDescription('Get next Love Live! event.'))
		.addSubcommand(subcommand => 
			subcommand.setName('inmonth').setDescription('Get events in a specific month')
				.addIntegerOption(o => o.setName('month').setDescription('month to get event').setRequired(true))),
	async execute(interaction) {
		await interaction.deferReply();
		const subcommand = interaction.options.getSubcommand();

		// Get next event
		if (subcommand == 'next') {
			const nextEvents = await Event.fetchNextEvents(true);
			const embeds = await Generator.generateNotifEmbeds(nextEvents);
			await interaction.reply({ embeds: embeds });
	
			// Add picture
			for (const [index, row] of nextEvents.entries()) {
				var thumbnailUrl = await thumbnailGetter(row);
				embeds[index].setImage(thumbnailUrl);
			}
			await interaction.editReply({ embeds: embeds });
		} 
		// Get events in a specific month
		else if (subcommand == 'inmonth') {
			let month = interaction.options.getInteger('month');
			if (!month) {
				month = (new Date()).getMonth();
			}
			const events = await Event.fetchEventInMonth(month);
			await interaction.editReply(codeBlock(TableGenerator(events, month)));
		}
	},
};