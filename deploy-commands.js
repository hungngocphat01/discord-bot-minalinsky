// Init database and import settings
require('dotenv').config();
global.logger = console.log;
const configLoader = require('./model/getconfig');

(async() => {
	console.log('Waiting for database...');
	const config = await configLoader();
	global.botConfig = config;
	console.log('Config loaded.');
	
	const fs = require('fs');
	const { REST } = require('@discordjs/rest');
	const { Routes } = require('discord-api-types/v9');
	
	const clientId = process.env.CLIENT_ID;
	const guildId = process.env.GUILD_ID;
	const token = process.env.BOT_TOKEN;
	
	// Get all modules 
	const COMMANDS_DIR = "./controller/commands";
	const commandData = [];
	const permissionData = {};
	const modules = fs.readdirSync(COMMANDS_DIR);
	
	modules.forEach((module) => {
		console.log(`Loaded module: ${module}`);
		const moduleFiles = fs.readdirSync(`${COMMANDS_DIR}/${module}`);
	
		for (const file of moduleFiles) {
			const command = require(`${COMMANDS_DIR}/${module}/${file}`);
			commandData.push(command.data.toJSON());
	
			// If command has non-default permissions specified
			const commandPerms = command.permissions;
			if (commandPerms) {
				const commandName = command.data.name;
				permissionData[commandName] = commandPerms;
			}
		}
	});
	// Write permisison data	
	console.log(permissionData);

	// Init REST API
	const rest = new REST({ version: '9' }).setToken(token);

	// Register commands
	try {
		await rest.put(
			Routes.applicationGuildCommands(clientId, guildId),
			{ body: commandData },	
		);

		console.log('Successfully registered application commands.');
	} catch (error) {
		console.error(error);
	}

	// Register permissions
	try {
		// Get all commands with ID
		const commands = await rest.get(
			Routes.applicationGuildCommands(clientId, guildId)
		);
		
		// Associate permissions with id
		const permissionRequestData = [];
		for (const command of commands) {
			const name = command.name;
			const id = command.id;
			const permissions = permissionData[name];
			// Skip configuring if command does not have permission
			if (!permissions) continue;
			permissionRequestData.push({
				id: id,
				permissions: permissions
			});
		}

		await rest.put(
			Routes.guildApplicationCommandsPermissions(clientId, guildId),
			{ body: permissionRequestData }
		);

		console.log(`Registered permissions.`)
	} catch (error) {
		console.error(error);
	}


})();
