const fs = require('fs');
const { REST } = require('@discordjs/rest');
const { Routes } = require('discord-api-types/v9');
require('dotenv').config();

const clientId = process.env.CLIENT_ID;
const guildId = process.env.GUILD_ID;
const token = process.env.BOT_TOKEN;

// Get all modules 
const COMMANDS_DIR = "./controller/commands";
const commands = [];
const modules = fs.readdirSync(COMMANDS_DIR);
modules.forEach((module) => {
	console.log(`Loaded module: ${module}`);
	const moduleFiles = fs.readdirSync(`${COMMANDS_DIR}/${module}`);

	for (const file of moduleFiles) {
		const command = require(`${COMMANDS_DIR}/${module}/${file}`);
		commands.push(command.data.toJSON());
	}
});

const rest = new REST({ version: '9' }).setToken(token);

(async () => {
	try {
		await rest.put(
			Routes.applicationGuildCommands(clientId, guildId),
			{ body: commands },
		);

		console.log('Successfully registered application commands.');
	} catch (error) {
		console.error(error);
	}
})();