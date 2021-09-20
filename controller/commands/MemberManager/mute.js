const { SlashCommandBuilder, codeBlock } = require('@discordjs/builders');
const AdminTools = require('../../../model/admin');
const TimeConverter = require('../../../view/convert-time');
const MuteEmbed = require('../../../view/generate-mute-info');

const commandData = {
	data: new SlashCommandBuilder()
		.setName('mute')
        .setDefaultPermission(false)
		.setDescription('Mute a member')
        .addSubcommand(subcommand => 
            subcommand
                .setName('set')
                .setDescription('Mute a member')
                .addUserOption(o => o.setName('member').setDescription('Member to mute').setRequired(true))
                .addIntegerOption(o => o.setName('time').setDescription('Time to mute').setRequired(true))
                .addStringOption(o => o.setName('unit').setDescription('Unit of time (min, hour, ...)').addChoices([['hour', 'hour'], ['minute', 'minute'], ['day', 'day']]).setRequired(true))
                .addStringOption(o => o.setName('reason').setDescription('Reason to mute'))
        )
        .addSubcommand(subcommand => 
            subcommand
                .setName('unset')
                .setDescription('Unmute a member')
                .addUserOption(o => o.setName('member').setDescription('Member to unmute').setRequired(true)))
        .addSubcommand(subcommand =>
            subcommand 
            .setName('list')
            .setDescription('List all members that are being muted')
        ),
	async execute(interaction) {
        await interaction.deferReply();

        const subCommand = interaction.options.getSubcommand();
        const member = interaction.options.getMember('member');
        const time = interaction.options.getInteger('time');
        const unit = interaction.options.getString('unit');
        let reason = interaction.options.getString('reason');
        reason = reason ? reason : 'Not defined';

        // ========================= MUTE SET =========================
        if (subCommand == 'set') {
            const id = member.id;
            const secs = TimeConverter.toSeconds(time, unit);

            // Call database
            const mute = await AdminTools.muteMember(id, reason, secs);
            if (!mute) {
                await interaction.editReply(codeBlock(`Member is already muted. Please unmute to change time.`));
                return;
            }
            
            // Call Discord API
            const muteRole = interaction.guild.roles.cache.find(r => r.id == global.botConfig['server-mute-role']);
            await member.roles.add(muteRole);
            
            // Generate embed
            const muteInfo = {
                display_name: member.displayName,
                color: member.roles.highest.color,
                begin_time: new Date(),
                reason: reason,
                secs_left: secs,
                avatar: member.user.avatarURL()
            };
            const embed = MuteEmbed.generateMuteEmbed(muteInfo);
            await interaction.editReply({ embeds: [embed] });
        }
        // ========================= MUTE UNSET =========================
        else if (subCommand == 'unset') {
            const id = member.id;
            const secs = TimeConverter.toSeconds(time, unit);

            // Call database
            const unmute = await AdminTools.unmuteMember(id);
            if (!unmute) {
                await interaction.editReply(codeBlock(`Member not muted. Cannot unmute.`));
                return;
            }

            const muteRole = interaction.guild.roles.cache.find(r => r.id == global.botConfig['server-mute-role']);
            await member.roles.remove(muteRole);
            await interaction.editReply(codeBlock(`Unmuted '${member.displayName}'`));
        }
        // ========================= MUTE LIST =========================
        else {
            const muteList = await AdminTools.listMutedMembers();  
            if (!muteList || muteList.length == 0) {
                await interaction.editReply(codeBlock('No one is being muted'));
                return;
            }

            // Set display_name and calculate secs_left
            for (const entry of muteList) {
                const member = await interaction.guild.members.fetch(entry['userid']);
                entry['display_name'] = member.displayName;
                entry['color'] = member.roles.highest.color;
                entry['avatar'] = member.user.avatarURL();
                
                let endTime = entry['begin_time'];
                endTime.setSeconds(endTime.getSeconds() + entry['interval']);

                entry['secs_left'] = (endTime - new Date())/1000;
            }
            
            // Generate embed and send back to client
            const embeds = MuteEmbed.generateMuteEmbeds(muteList);
            await interaction.editReply({ embeds: embeds });
        }
	},
    permissions: [
        {
            id: global.botConfig['server-owner-id'], // My ID
            type: 2, // 2: USER, 1: ROLE
            permission: true
        }
    ],
}

// Admins can also use this role
for (const id of global.botConfig['admin-roles-ids']) {
    commandData.permissions.push({
        id: id,
        type: 1, // 1: ROLE
        permission: true
    });
}

module.exports = commandData;