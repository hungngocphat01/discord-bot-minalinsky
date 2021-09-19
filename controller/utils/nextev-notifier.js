const Event = require('../../model/events');
const Generator = require('../../view/notification-generator')

// Decide to send message into 'bộ chính trị' or 'thông báo'
function decideChannel(eventDate, today) {
    const diffMS = eventDate - today;
    const oneDay = 24 * 60 * 60 * 1000;

    // Model API guarantees dayDiff >= 0
    const dayDiff = diffMS/oneDay;
    console.log('Daydiff: ', dayDiff);
    
    if (dayDiff <= 1.5 && dayDiff > 0) {
        return [global.botConfig['notify-channel-id'], true];
    } else if (dayDiff <= 2.5) {
        return [global.botConfig['pre-notify-channel-id'], false];
    }
    return [null, false];
}

function notifier (client) {
    Event.fetchNextEvents().then(async (events) => {
        logger(`Next events: ${events.length}`);
        logger(JSON.stringify(events));
        
        if (events.length > 0) {
            const today = new Date();
            // In Date constructor: month 0 means Jan
            const eventDate = new Date(today.getFullYear(), events[0].month - 1, events[0].day);

            // Calculate date to decide channel
            let [ channelID, mark ] = decideChannel(eventDate, today);
            if (channelID == null) {
                logger('Event(s) too far away. Not sending.');
                return;
            }

            // Debugging on local machine
            if (process.env.RUNNING_ON_HEROKU != 1) {
                channelID = global.botConfig['debug-channel-id']; 
            }

            // Fetch channel to send
            const guild = await client.guilds.fetch(process.env.GUILD_ID);
            const channel = await guild.channels.fetch(channelID.toString());

            logger(`Sending event(s) to ${channel.name}`);

            const embeds = Generator.generateNotifEmbeds(events);
            await channel.send({ embeds: embeds });
            logger(`Sent.`);

            // Whether to mark event as notified (sent to main notif channel)
            if (mark) {
                await Event.markAsNotified(events);
            }
        }
    });
}

module.exports = notifier;