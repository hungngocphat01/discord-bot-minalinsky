const pool = require('./dbpool');
require('dotenv').config();

async function fetchAllEvents() {
    const query = {
        text: 'select * from events;',
    };
    const result = await pool.query(query);
    return result;
}

async function fetchNearestDate() {
    const year = (new Date()).getFullYear();
    const query = {
        text: `
            select day, month
            from events
            where make_date($1, month, day) > current_date;
        `,
        values: [year]
    }
    const result = await pool.query(query);
    if (result.rowCount == 0) {
        throw Error(`Cannot get next day. Maybe end of year.`);
    }
    return result.rows[0];
}

async function fetchNextEvent(notitfied) {
    const nextdate = await fetchNearestDate();
    const query = {
        text: `
            select *
            from events
            where day=$1 and month=$2;
        `,
        values: [nextdate.day, nextdate.month]
    };
    const result = await pool.query(query);
    return result.rows.filter(row => row.notitfied == notitfied);
}

module.exports = {
    fetchAllEvents,
    fetchNearestDate,
    fetchNextEvent
};