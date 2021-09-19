const nextEventNotifier = require('../utils/nextev-notifier');

module.exports = {
	name: 'ready',
	once: true,
	execute(client) {
		nextEventNotifier(client);
		logger(`Ready! Logged in as ${client.user.tag}`);
	},
};