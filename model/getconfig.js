const pool = require('./dbpool');

async function getConfig() {
    const result = await pool.query("select * from settings;");
    return Object.fromEntries(
        result.rows.map(row => [row.field, row.value])
    );
}

module.exports = getConfig;