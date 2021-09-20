const { parse } = require("dotenv");

const secHour = 3600;
const secMinute = 60;
const minuteHour = 60;
const hourDay = 24;
const secDay = secHour * hourDay;

function parseHumanReadableToSeconds(amount, unit) {
    switch (unit) {
        case 'minute': return Math.floor(amount * secMinute);
        case 'hour': return Math.floor(amount * secHour);
        case 'day': return Math.floor(amount * secDay);
    }
}

function parseSecondsToMinute(seconds) {
    const minutes = seconds / secMinute;
    const remainingSecs = (minutes - Math.floor(minutes)) * secMinute;
    return `${Math.floor(minutes)} mins ${Math.floor(remainingSecs)} secs`
}

function parseSecondsToHour (seconds) {
    const hours = seconds / secHour;
    const minutes = parseSecondsToMinute((hours - Math.floor(hours)) * secHour);
    return `${Math.floor(hours)} hrs ${minutes}`;
}

function parseSecondsToDay (seconds) {
    const days = seconds / secDay;
    const hours = parseSecondsToHour((days - Math.floor(days)) * secDay);
    return `${Math.floor(days)} days ${hours}`;
}

function parseSecondToHumanReadable(seconds) {
    if (seconds < secHour) {
        return parseSecondsToMinute(seconds);
    }
    else if (seconds < secDay) {
        return parseSecondsToHour(seconds);
    }
    else {
        return parseSecondsToDay(seconds);
    }
}

module.exports = {
    toSeconds: parseHumanReadableToSeconds,
    fromSeconds: parseSecondToHumanReadable
};