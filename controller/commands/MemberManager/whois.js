const { SlashCommandBuilder, codeBlock } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('whois')
		.setDescription('Get information of a user.')
        .addUserOption(o => o.setName('user').setDescription('User to get information').setRequired(true)),
	async execute(interaction) {
		const member = await interaction.options.getMember('user').fetch();
		const memberRoles = member.roles.cache.map(r => r.toString()).join(' ');
		const memberPresence = member.presence;

        const embed = new MessageEmbed()
			.setAuthor(member.user.username.toString())
			.setImage(member.user.displayAvatarURL({ size: 2048 }))
			.setColor(member.roles.highest.color)
			.addField("Display name", member.toString())
			.addField("Created on", member.user.createdAt.toDateString())
			.addField("Joined server on", member.joinedAt.toDateString())
			.addField("Roles", memberRoles)
			.addField("Booster", (member.premiumSince != undefined) ? "Yes" : "No")
			.addField("Status", memberPresence == undefined ? "Offline" : "Online");
	
		await interaction.reply( { embeds: [embed] });
	}		
};