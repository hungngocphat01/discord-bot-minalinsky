const pool = require('./dbpool');

async function listMutedMembers() {
    const query = {
        text: `
            select *
            from muted
            where active='t'
            order by begin_time asc;`,
    }
    const result = await pool.query(query);
    return result.rows;
}

async function muteMember(uid, reason, interval) {
    // User cant be muted twice
    const muteList = await listMutedMembers();
    const member = muteList.find(m => m.userid == uid);
    if (member) {
        return null;
    }

    const query = {
        text: `
            insert into muted (userid, begin_time, reason, interval, active)
            values ($1, current_timestamp, $2, $3, 't');
        `, 
        values: [uid.toString(), reason, interval]
    };
    await pool.query(query);
    return true;
}

async function unmuteMember(uid) {
    const muteList = await listMutedMembers();
    const member = muteList.find(m => m.userid == uid);
    if (!member) {
        return null;
    }

    // High level API constraint: user cant be muted twice, so this works
    const query = {
        text: `
            update muted 
            set active='f'
            where userid=$1;
        `,
        values: [uid.toString()]
    }
    await pool.query(query);
    return true;
}

module.exports = {
    listMutedMembers,
    muteMember,
    unmuteMember
}