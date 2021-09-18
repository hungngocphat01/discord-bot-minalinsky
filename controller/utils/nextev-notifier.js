const Event = require('../../model/events');

function notifier (client) {
    Event.fetchNextEvent().then((events) => {
        console.log('Next events');
        console.log(events);
    });
}

module.exports = notifier;