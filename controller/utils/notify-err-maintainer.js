module.exports = async function notifyMaintainer(client, err, interaction) {
    const guild = await client.guilds.fetch(process.env.GUILD_ID);
    const owner = await guild.fetchOwner();	
    if (!interaction) {
        const debugChannel = await guild.channels.fetch(global.botConfig['debug-channel-id']);
        await debugChannel.send(`${owner}` + `${err}`);
    }
    else if (interaction) {
        await interaction.reply(`${owner}` + `${err}`);
    }
};