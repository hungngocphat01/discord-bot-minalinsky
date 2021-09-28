const nextEventNotifier = require('../utils/nextev-notifier');
const muteClockCallback = require('../utils/muteclock');
const { codeBlock } = require('@discordjs/builders');
const MaintainerNotifier = require('../utils/notify-err-maintainer');

module.exports = {
	name: 'ready',
	once: true,
	execute(client) {
		// Send next event
		try {
			nextEventNotifier(client);
		}
		catch (error) {
			logger(`Cannot send next event. Error: ${error}`);
			MaintainerNotifier(client, codeBlock(`Cannot send next event. ${error}`)).then(v => logger(`Error sent`));
		}
		
		// Start mute checker 
		setInterval(() => muteClockCallback(client), 60000);	

		logger(`Ready! Logged in as ${client.user.tag}`);
	},
};