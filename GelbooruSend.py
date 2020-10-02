import discord
from discord.ext import commands
import pygelbooru
from BasicDefinitions import COMMAND_PREFIX

# Init the Danbooru client
client = pygelbooru.Gelbooru()

class GelbooruSend(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Module loaded: GelbooruSend")
    
    @commands.command()
    async def art(self, ctx, tags = None, num = 1):
        print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
        if tags is not None:
            tagsLst = tags.split("|")
            tagsLst.append("rating:safe")
    
            if num > 5:
                await ctx.send("```To avoid spamming, only 5 images is accepted.```")
            else:
                for i in range(0, num):
                    result = await client.random_post(tags = tagsLst)
                    embed = discord.Embed()
                    embed.set_image(url = str(result))
                    try:
                        await ctx.send(embed = embed)
                    except Exception:
                        # Send error message
                        await ctx.send("```Error: no image found or tags were not correctly specified. Please notice that the character names are written in East Asian order. For example: kousaka_honoka, not honoka_kosaka.```")
                        break
        else:
            # Send help
            helpStr = f"""```
art command usage
This command is used to get a number of images from Gelbooru (safe only).

Syntax: {COMMAND_PREFIX}art <tags> [<number of images> nsfw]

<tags>: can be one or more. If there is more than one tag, join them with a | character.
Example: kousaka_honoka|minami_kotori|yuri
Tags could be:
- Series name: love_live!, love_live!_sunshine!!, bang ...
- Character name: kousaka_honoka, nishikino_maki, hoshizora_rin, ... 
- Many other types of tags.

<number of images>: an integer represents number of images. Must be smaller or equal to 5.

Examples: 
{COMMAND_PREFIX}art kousaka_honoka|sonoda_umi 5
{COMMAND_PREFIX}art kousaka_honoka|nishikino_maki```"""
            await ctx.send(helpStr)


    @commands.command()
    async def hentai(self, ctx, tags = None, num = 1):
        print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")

        if tags is not None:
            if not ctx.channel.nsfw:
                await ctx.send("```This command cannot be issued in a non-nsfw channel.```")
                return

            tagsLst = tags.split("|")
            tagsLst.append("-rating:safe")
            
            if num > 5:
                await ctx.send("```To avoid spamming, only 5 images is accepted.```")
            else:
                for i in range(0, num):
                    result = await client.random_post(tags = tagsLst)
                    embed = discord.Embed()
                    embed.set_image(url = str(result))
                    try:
                        await ctx.send(embed = embed)
                    except Exception:
                        # Send error message
                        await ctx.send("```Error: no image found or tags were not correctly specified.\nPlease notice that the character names are written in East Asian order. For example: kousaka_honoka, not honoka_kosaka.\nAlso make sure the franchise's name is correctly written. For example: love_live!, not love_live.```")
                        break
        else:
            # Send help
            helpStr = f"""```
hentai command usage
This command is used to get a number of images from Gelbooru (guaranteed to be nsfw).

Syntax: {COMMAND_PREFIX}hentai <tags> [<number of images>]

<tags>: can be one or more. If there is more than one tag, join them with a | character.
Example: kousaka_honoka|minami_kotori|yuri
Tags could be:
- Series name: love_live!, love_live!_sunshine!!, bang ...
- Character name: kousaka_honoka, nishikino_maki, hoshizora_rin, ... 
- Many other types of tags.

<number of images>: an integer represents number of images. Must be smaller or equal to 5.

Examples: 
{COMMAND_PREFIX}hentai kousaka_honoka
{COMMAND_PREFIX}hentai kousaka_honoka|nishikino_maki```"""
            await ctx.send(helpStr)