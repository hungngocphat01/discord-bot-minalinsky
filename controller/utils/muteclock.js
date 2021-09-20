// Contains a clock that check for any muted person every 1 minutes
const AdminTools = require('../../model/admin');

async function mutedPeriodicCheckCallback(client) {
    // Get all muted members
    const muteList = await AdminTools.listMutedMembers();
    if (!muteList || muteList.length == 0) {
        return;
    }

    for (const entry of muteList) {
        const { userid, interval, begin_time } = entry;

        let endTime = entry['begin_time'];
        endTime.setSeconds(endTime.getSeconds() + interval);
        const remaining = endTime - new Date();
        
        if (remaining < 60000) {
            // Call database
            const unmute = await AdminTools.unmuteMember(userid);
            // Call API
            const guild = await client.guilds.fetch(process.env.GUILD_ID);
            const muteRole = guild.roles.cache.find(r => r.id == global.botConfig['server-mute-role']);
            const user = await guild.members.fetch(userid);
            await user.roles.remove(muteRole);
            logger(`Unmuted ${userid} automatically`);
        }
    }
}

module.exports = mutedPeriodicCheckCallback;