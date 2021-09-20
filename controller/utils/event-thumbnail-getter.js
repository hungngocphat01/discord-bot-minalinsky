var Scraper = require('images-scraper');

const google = new Scraper({
  puppeteer: {
    headless: true,
  },
});

async function get(keyword, site, limit) {
    const results = await google.scrape(`${keyword} site:${site}`, limit);
    return results;
}

module.exports = async function(event) {
    if(event['specific_source']) {
        return event['source'];
    }
    const stablizer = (event['type'] == 'BD') ? ' card' : '';
    const images = await get(event['details'] + stablizer, event['source'], 10);
    const randomIndex = Math.floor(Math.random() * images.length);
    return images[randomIndex]['url'];
};