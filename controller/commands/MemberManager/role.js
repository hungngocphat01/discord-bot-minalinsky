const { SlashCommandBuilder, codeBlock } = require('@discordjs/builders');
const Event = require('../../../model/events');
const Generator = require('../../../view/notification-generator');

const commandData = {
	data: new SlashCommandBuilder()
		.setName('role')
        .setDefaultPermission(false)
		.setDescription('Give or delete role of a member')
        .addSubcommand(subcommand => 
            subcommand
                .setName('give')
                .setDescription('Give role to a user')
                .addRoleOption(o => o.setName('role').setDescription('Role to give').setRequired(true))
                .addUserOption(o => o.setName('member').setDescription('Member to give role to').setRequired(true))
        )
        .addSubcommand(subcommand => 
            subcommand
                .setName('delete')
                .setDescription('Delete role from a user')
                .addRoleOption(o => o.setName('role').setDescription('Role to delete').setRequired(true))
                .addUserOption(o => o.setName('member').setDescription('Member to delete role from').setRequired(true))
        ),
	async execute(interaction) {
        const subCommand = interaction.options.getSubcommand();
        const user = interaction.options.getMember('member');
        const role = interaction.options.getRole('role');

        if (subCommand == 'give') {
            await user.roles.add(role);
            await interaction.reply(codeBlock(`Gave role ${role.name} to ${user.displayName}`));
        } 
        else if (subCommand == 'delete') {
            await user.roles.remove(role);
            await interaction.reply(codeBlock(`Deleted role ${role.name} to ${user.displayName}`));
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