const { MessageEmbed } = require("discord.js");

// Function to generate one embed
function generateEmbed(event) {
    let type = '';
    switch (event.type) {
        case 'BD': type = 'Sinh nhật'; break;
        case 'AN': type = 'Anime'; break;
        case 'SP': type = 'Ngày đặc biệt'; break;
        case 'PV': type = 'Promotional Video (PV)'; break;
        case 'RE': type = 'Album/single'; break;
        default: type = 'Sự kiện không xác định'; break;
    }
    let title = event['details'];
    let note = event['note'];
    let date = `Ngày ${event['day']} tháng ${event['month']}`;
    if (note.length == 0) 
        note = "Không";
    
    const embed = new MessageEmbed()
        .setAuthor(type)
        .setTitle(title)
        .setDescription(date)
        .addField('Chú thích', note);
    return embed;
}

// Function to generate multiple embeds
function generateEmbeds(events) {
    const embeds = [];
    events.forEach(event => {
        const embed = generateEmbed(event);
        embeds.push(embed);
    });
    return embeds;
}

module.exports = {
    generateNotifEmbed: generateEmbed,
    generateNotifEmbeds: generateEmbeds
};