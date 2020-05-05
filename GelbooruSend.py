import discord
from discord.ext import commands
import pygelbooru
from BasicDefinitions import COMMAND_PREFIX

# Init the Danbooru client
client = pygelbooru.Gelbooru()

class GelbooruSend(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def art(self, ctx, tags = None, num = 1, nsfw = ""):
        print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
        if tags is not None:
            tagsLst = tags.split("|")
            if ("nsfw" not in nsfw.lower()):
                tagsLst.append("rating:safe")
            if ("nsfw" in nsfw.lower() and not ctx.channel.nsfw):
                await ctx.send("```You allowed nsfw images. This option only available in nsfw channels.```")
            else:
                if num > 5:
                    await ctx.send("```To avoid spamming, only 5 images is accepted.```")
                else:
                    for i in range(0, num):
                        result = await client.random_post(tags = tagsLst)
                        embed = discord.Embed()
                        embed.set_image(url = str(result))
                        await ctx.send(embed = embed)
        else:
            # Send help
            helpStr = f"""```
art command usage
This command is used to get a number of images from Gelbooru.

Syntax: {COMMAND_PREFIX}art <tags> [<number of images> nsfw]

<tags>: can be one or more. If there is more than one tag, join them with a | character.
Example: kousaka_honoka|minami_kotori|yuri

<number of images>: an integer represents number of images. Must be smaller or equal to 5.

<nsfw>: specify whether nsfw images are accepted or not. 
If its value is 'nsfw', returned images can randomly be either safe or not safe.
You have to specify number of images before toggling the nsfw option.
Only available in nsfw channel.

Examples: 
{COMMAND_PREFIX}art kousaka_honoka|sonoda_umi 5
{COMMAND_PREFIX}art kousaka_honoka|nishikino_maki 1 nsfw```"""
            await ctx.send(helpStr)

