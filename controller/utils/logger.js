const LogDB = require('../../model/logging');

function writeLog(...args) {
    const str = args.join(' ');
    console.log(str);
    LogDB(str);
}

module.exports = writeLog;