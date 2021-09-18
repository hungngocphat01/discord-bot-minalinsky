const { Pool } = require('pg');
require('dotenv').config({ path: '../.env' });

const connectionString = process.env.DB_URL;

console.log('Database is being initialized...');
let pool = new Pool({
    connectionString,
});

module.exports = pool;