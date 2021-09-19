const { codeBlock } = require('@discordjs/builders');

module.exports = {
	name: 'messageCreate',
	async execute(message) {
		if (global.botStatus.debug_mode == true) {
			return;
		}
	},
};