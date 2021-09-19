const configLoader = require('../../model/getconfig');

configLoader().then(config => {
    global.botConfig = config;
    global.botStatus.databaseState = true;
    logger('Bot config loaded to memory.');
}).catch(err => 
    console.log(`Cannot load config: ${err.stack}`)
);