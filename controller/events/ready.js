const nextEventNotifier = require('../utils/nextev-notifier');

module.exports = {
	name: 'ready',
	once: true,
	execute(client) {
		nextEventNotifier(client);
		console.log(`Ready! Logged in as ${client.user.tag}`);
	},
};