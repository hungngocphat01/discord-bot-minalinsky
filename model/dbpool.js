const { Pool } = require('pg');
const connectionString = process.env.DATABASE_URL;

console.log('Database is being initialized...');
let pool = new Pool({
    connectionString,
    ssl: {
        rejectUnauthorized: false
    }
});

pool.once('connect', client => {
    logger('Database connection established.');
});

module.exports = pool;