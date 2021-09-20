const { MessageEmbed } = require("discord.js");
const thumbnailGetter = require('../controller/utils/event-thumbnail-getter');

// Generate info for birthday
function generateEmbedBD(event) {
    return {
        event_type: 'Sinh nhật',
        title: event['details'],
        note: event['note'] ?? 'Không',
        note_field: 'Chú thích'
    };
}

// Generate info for PV
function generateEmbedPV(event) {
    return {
        event_type: 'Ra mắt album',
        title: event['details'],
        note: event['note'] ?? 'Không',
        note_field: 'Năm ra mắt'
    };
}

// Generate info for birthday
function generateEmbedSP(event) {
    return {
        event_type: 'Sự kiện đặc biệt',
        title: event['details'],
        note: event['note'] ?? 'Không',
        note_field: 'Năm xảy ra'
    };
}


// Function to generate one embed
async function generateEmbed(event, getThumbnail) {
    if (event.type == 'BD') {
        var { event_type, title, note, note_field } = generateEmbedBD(event);
    }
    else if (event.type == 'SP') {
        var { event_type, title, note, note_field } = generateEmbedSP(event); 
    }
    else if (event.type == 'PV') {
        var { event_type, title, note, note_field } = generateEmbedPV(event); 
    }

    let date = `Ngày ${event['day']} tháng ${event['month']}`;
    let embed = new MessageEmbed()
        .setAuthor(event_type)
        .setTitle(title)
        .setDescription(date)
        .addField(note_field, note)
        .setFooter('Sự kiện sắp xảy ra');

    if (getThumbnail) {
        try {
            var thumbnailUrl = await thumbnailGetter(event);
            console.log(`Thumbnail arrived: ${thumbnailUrl}`);
            embed = embed.setImage(thumbnailUrl);
        }
        catch (err) {
            logger(`Cannot get thumbnail. Ignoring...\n${err}`);
        }
    } 
    return embed;
}

// Function to generate multiple embeds
/** 
 * getThumbnail: whether to get thumbnail TOGETHER with generating the embed or not
 * Takes time. Should be used with sending notification, not for /nextev
 * **/
async function generateEmbeds(events, getThumbnail = false) {
    const embeds = [];
    for (const event of events) {
        const embed = await generateEmbed(event, getThumbnail);
        embeds.push(embed);
    }
    return embeds;
}

module.exports = {
    generateNotifEmbed: generateEmbed,
    generateNotifEmbeds: generateEmbeds
};