const { SlashCommandBuilder, codeBlock } = require('@discordjs/builders');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('eval')
		.setDescription('Evaluate a Node.js expression (owner only)')
        .addStringOption(
            o => o.setName('expr').setDescription('Node.js expression').setRequired(true)
        ),
	async execute(interaction) {
        const expr = interaction.options.getString('expr')
        const output = eval(expr);
        await interaction.reply(codeBlock(">> " + expr + "\n" + output.toString()));
	},
};