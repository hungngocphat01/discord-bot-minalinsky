const { MessageEmbed } = require("discord.js");
const TimeConverter = require('./convert-time');

//
//     {
//       display_name: 'abc',       (appended by controller)
//       secs_left: 123             (appended by controller)
//       userid: '1234',
//       begin_time: 2021-09-20T03:29:36.362Z,
//       reason: 'abc',
//       interval: 1234,
//       active: true
//     }
//

function generateMuteEmbed(row) {
    const { begin_time, reason, display_name, secs_left } = row;
    const embed = new MessageEmbed()
        .setAuthor(display_name)
        .addField('Time left', TimeConverter.fromSeconds(secs_left))
        .addField('Reason', reason)
        .addField('Muted since', begin_time.toString());
    return embed;
}

function generateMuteEmbeds(rows) {
    const embeds = [];
    for (const row of rows) {
        embeds.push(generateMuteEmbed(row));
    }
    return embeds;
}

module.exports = {
    generateMuteEmbed,
    generateMuteEmbeds
}