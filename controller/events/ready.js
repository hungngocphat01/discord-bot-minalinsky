const nextEventNotifier = require('../utils/nextev-notifier');
const muteClockCallback = require('../utils/muteclock');

module.exports = {
	name: 'ready',
	once: true,
	execute(client) {
		// Send next event
		nextEventNotifier(client);
		// Start mute checker 
		setInterval(() => muteClockCallback(client), 60000);		

		logger(`Ready! Logged in as ${client.user.tag}`);
	},
};