const { SlashCommandBuilder, codeBlock } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');
const { promisify } = require('util');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('stats')
		.setDescription('Get information about current server.'),
	async execute(interaction) {
		// Fetch guild
		const guild = await interaction.guild.fetch();
		
		// Get information
		const members = await guild.members.fetch();
		let boosters = members.filter((mem) => mem.premiumSinceTimestamp != undefined);
		boosters = boosters.map(m => m.toString());
		boosters = boosters.size > 0 ? boosters.join(` `) : 'None';

		const channelCount = (await interaction.guild.channels.fetch()).size;
		const nonBotOnlineMembers = members.filter((mem) => !mem.user.bot && (mem.presence != undefined));
		const botMembers = members.filter(mem => mem.user.bot);
		const owner = await guild.fetchOwner();

		const embed = new MessageEmbed()
			.setAuthor(interaction.guild.name, interaction.guild.iconURL({ size: 2048 }))
			.addField("Channels", channelCount.toString(), true)
			.addField("Members", guild.approximateMemberCount.toString(), true)
			.addField("Online members (non-bot)", nonBotOnlineMembers.size.toString(), false)
			.addField("Bot members: ", botMembers.size.toString(), true)
			.addField("Contributors", boosters, false)
			.addField("Boost level", guild.premiumTier.toString(), true)
			.addField("Boost quantity", guild.premiumSubscriptionCount.toString(), true)
			.addField("Owner", owner.toString())
			.setImage(interaction.guild.iconURL());
		await interaction.reply({ embeds: [embed] });
	},
};