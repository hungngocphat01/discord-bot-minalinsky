// Require the necessary discord.js classes
const { Client, Collection, Intents } = require('discord.js');
const fs = require('fs');
const botintro = require('./controller/utils/botintro');
require('dotenv').config();

console.log(botintro.getHeader());

// Initialize client
const token = process.env.BOT_TOKEN;

const client = new Client({ intents: [
	Intents.FLAGS.GUILDS, 
	Intents.FLAGS.GUILD_MEMBERS, 
	Intents.FLAGS.GUILD_MESSAGE_REACTIONS, 
	Intents.FLAGS.DIRECT_MESSAGE_REACTIONS, 
	Intents.FLAGS.GUILD_PRESENCES, 
	Intents.FLAGS.GUILD_EMOJIS_AND_STICKERS
] });
global.botStatus = {
    start_time: (new Date()).toDateString(),
    on_heroku: process.env.RUNNING_ON_HEROKU,
};
module.exports.client = client;

// Get all modules 
const COMMANDS_DIR = "./controller/commands";
client.commands = new Collection();
const modules = fs.readdirSync(COMMANDS_DIR);
modules.forEach((module) => {
	console.log(`Loaded module: ${module}`);
	const moduleFiles = fs.readdirSync(`${COMMANDS_DIR}/${module}`);

	for (const file of moduleFiles) {
		const command = require(`${COMMANDS_DIR}/${module}/${file}`);
		client.commands.set(command.data.name, command);
	}
});

// Register events
const eventFiles = fs.readdirSync('./controller/events').filter(file => file.endsWith('.js'));
for (const file of eventFiles) {
	const event = require(`./controller/events/${file}`);
	if (event.once) {
		client.once(event.name, (...args) => event.execute(...args));
	} else {
		client.on(event.name, async (...args) => event.execute(...args));
	}
}

client.login(token);