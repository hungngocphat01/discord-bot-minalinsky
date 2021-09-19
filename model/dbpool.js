const { Pool } = require('pg');
const connectionString = process.env.DB_URL;

console.log('Database is being initialized...');
let pool = new Pool({
    connectionString,
});

pool.once('connect', client => {
    logger('Database connection established.');
});

module.exports = pool;