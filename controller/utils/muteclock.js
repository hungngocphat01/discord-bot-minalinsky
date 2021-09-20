// Contains a clock that check for any muted person every 1 minutes
const AdminTools = require('../../model/admin');

async function mutedPeriodicCheckCallback() {
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
            logger(`Unmuted ${userid} automatically`);
        }
    }
}

module.exports = mutedPeriodicCheckCallback;