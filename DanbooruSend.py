import discord
from discord.ext import commands
from pybooru import Danbooru
from BasicDefinitions import COMMAND_PREFIX

# Init the Danbooru client
client = Danbooru("danbooru")

class DanbooruSend(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def danbooru(self, ctx, tag = None, num = 1, safe = True):
        if tag == None:
            helpStr = f"""```danbooru command usage
{COMMAND_PREFIX}danbooru <tag>
Due to limitation of Danbooru, only one tag is accepted (the other tag is rating:safe)
Tags could be:
- Series name: love_live!, love_live_sunshine!! ...
- Character name: kousaka_honoka, nishikino_maki, hoshizora_rin, ... 
- Many other types of tags.```"""
            await ctx.send(helpStr)
        else:
            if num <= 6:
                if (type(safe) is bool and safe):
                    posts = client.post_list(limit = num, random = True, tags = f"{tag} rating:safe")
                else:
                    posts = client.post_list(limit = num, random = True, tags = f"{tag}")
                if len(posts) == 0:
                    ctx.send(f"```No post found with tag(s): {tag}```")
                else:
                    for post in posts:
                        embed = discord.Embed()
                        embed.set_image(url = post['file_url'])
                        await ctx.send(embed = embed)
            else: 
                ctx.send("```Max combo allowed is 6.```")