const { table } = require('table');

function generate(events, month) {
    let tableArr = events.map(event => Object.values(event));
    tableArr = [Object.keys(events[0])].concat(tableArr);
    const config = {
        header: {
            alignment: 'center',
            content: `EVENTS IN MONTH: ${month}`,
        },
    }

    return table(tableArr, config);
}

module.exports = generate;