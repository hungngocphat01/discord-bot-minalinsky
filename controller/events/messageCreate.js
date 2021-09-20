const { codeBlock } = require('@discordjs/builders');

// React emoji to certain keywords (ponk, ...)
async function processEmojiKeywords(msgObj) {
	const activationThreshold = 0.6;
	if (Math.random() > activationThreshold) {
		return;
	}
	const msgString = msgObj.toString();
	// Fetch cached keyword list
	const keywordList = global.botConfig['emoji-react-signs'];
	// Check if each emoji is in the message
	const booleanMap = keywordList.map(keyword => msgString.toLowerCase().includes(keyword));
	// React
	for (const [index, value] of booleanMap.entries()) {
		if (value) {
			const emojiName = keywordList[index];
			const emoji = msgObj.guild.emojis.cache.find(emoji => emoji.name == emojiName);
			msgObj.react(emoji)
				.then(v => logger(`Reacted to ${msgString.substring(0, 30)}`))
				.catch(e => logger(`Failed to react emoji: ${emojiName}`));
		}
	}
}

// Reply to certain messages
async function processRandomReplies(msgObj) {
	// Get string
	const msgString = msgObj.toString();
	// Fetch cached responses -> array
	// Each pair of key-value: 'regex': ['threshold': float, 'responses': array]
	const keywordDataArr = global.botConfig['random-resp-signs'];
	const regexList = Object.keys(keywordDataArr);
	const booleanMap = regexList.map(regex => {
		const reg = new RegExp(regex, 'g');
		return reg.test(msgString.toLowerCase());
	});
	// Reply (only once)
	for (let [index, value] of booleanMap.entries()) {
		if (value) {
			const { threshold, replies } = keywordDataArr[regexList[index]];
			if (Math.random() > threshold) {
				return;
			}
			// Get random index in the responses list
			const randomIdx = Math.floor(Math.random() * replies.length);
			const reply = replies[randomIdx];

			await msgObj.reply(reply);
			logger(`Replied to ${msgString}`);
			return;
		}
	}
}

module.exports = {
	name: 'messageCreate',
	async execute(msgObj) {
		if (global.botStatus.debug_mode == true) {
			return;
		}
		try {
			await processEmojiKeywords(msgObj);
			await processRandomReplies(msgObj);
		} catch (e) {
			logger(`Error when try processing message: '${msgObj.toString().substring(0, 30)}' \nCallstack: ${e.stack}`)
			await MaintainerNotifier(msgObj.client, e).then(v => logger(`Error sent`));
		}
	},
};