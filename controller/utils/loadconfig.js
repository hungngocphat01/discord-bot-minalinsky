// Load bot config from database and save cache into memory
const configLoader = require('../../model/getconfig');

module.exports = async () => {
    // Temporarily set logger to console.log (ignore database connection)
    global.logger = console.log;
    const config = await configLoader();
    global.botConfig = config;
}