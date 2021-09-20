const { codeBlock } = require('@discordjs/builders');

module.exports = async function notifyMaintainer(client, err) {
    const guild = await client.guilds.fetch(process.env.GUILD_ID);
    const owner = await guild.fetchOwner();	
    const debugChannel = await guild.channels.fetch(global.botConfig['debug-channel-id']);
    await debugChannel.send(`${owner}` + codeBlock(`${err}`));
};