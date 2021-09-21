const pool = require('./dbpool');
require('dotenv').config();

async function fetchAllEvents() {
    const query = {
        text: 'select * from events;',
    };
    const result = await pool.query(query);
    return result.rows;
}

async function fetchEventInMonth(month) {
    const query = {
        text: `select day, type, details, note 
            from events 
            where month=$1
            order by day asc;`,
        values: [month]
    };
    const result = await pool.query(query);
    return result.rows; 
}

async function fetchNearestDate(all = false) {
    const year = (new Date()).getFullYear();
    const query = {
        text: '',
        values: [year]
    }
    // Whether to get all events or just unnotified ones
    if (all) {
        query.text = `
        select day, month
        from events
        where make_date($1, month, day) > current_date
        order by month, day;`;
    }
    else {
        query.text = `
        select day, month
        from events
        where make_date($1, month, day) > current_date and notified='f'
        order by month, day;`;
    }

    const result = await pool.query(query);
    if (result.rowCount == 0) {
        console.log('No next date to query. See you next year ;)');
        return null;
    }
    return result.rows[0];
}

async function fetchNextEvents(all = false) {
    const nextdate = await fetchNearestDate(all);
    if (nextdate == null) {
        return [];
    }
    const query = {
        text: `
            select *
            from events
            where day=$1 and month=$2;`,
        values: [nextdate.day, nextdate.month]
    };
    const result = await pool.query(query);
    return result.rows;
}

async function markAsNotified(events) {
    events.forEach(event => {
        const query = {
            text: `
                update events
                set notified='t'
                where day=$1 and month=$2 and details=$3;`,
            values: [event.day, event.month, event.details]
        };
        pool.query(query).then(value => 
            logger(`Marked event as notified: [${event.type}] ${event.details}`)
        );
    });
}

module.exports = {
    fetchAllEvents,
    fetchNearestDate,
    fetchNextEvents,
    markAsNotified,
    fetchEventInMonth
};