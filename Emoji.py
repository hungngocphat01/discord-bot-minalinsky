import discord
from discord.ext import commands
import copy
import re
import json
from BasicDefinitions import COMMAND_PREFIX
from Logging import *

def similarityBetween(str1, str2):
    same = 0
    n1 = len(str1)
    n2 = len(str2)

    if n1 > n2:
        Range = range(0, n2)
    else:
        Range = range(0, n1)
    for i in Range:
        if str1[i] == str2[i]:
            same += 1
    return same

class Emoji(commands.Cog):
    def __init__(self, bot):
        log("Module loaded: Emoji")
        self.bot = bot
        with open("configuration.json", mode="rt") as f:
            self.emojson = json.loads(f.read())["custom_emojis"]

    # Send emoji
    @commands.command(aliases = ["emo"])
    async def emoji(self, ctx, emoname = None):
        command_log(ctx)
        if emoname == None:
            helpStr = f"""```Usage:
{COMMAND_PREFIX}emoji list: list all emoji names (text only).
{COMMAND_PREFIX}emoji <name>: send an emoji with given name.

    For preview of emojis, go to channel #usable-emoji```"""
            await ctx.send(helpStr)
        elif emoname.lower() == "list":
            emojilistStr = f"```Emoji list:\n\n"
            for key in self.emojson:
                emojilistStr += str(key) + "\n"
            emojilistStr += "```"
            await ctx.send(emojilistStr)
        else:
            command_log(ctx)  
            try:
                embed = discord.Embed()
                embed.set_author(name = ctx.message.author.display_name, icon_url = ctx.message.author.avatar_url)
                embed.set_image(url = str(self.emojson[emoname]))
                await ctx.message.delete()
                await ctx.send(embed = embed)        
            except KeyError:
                suggestions = []
                # Copy the emojson dictionary
                similars = copy.deepcopy(self.emojson)
                # With each emoji, find the similarity between its name and the input emoname
                # At the same time, find emojis whose name contains the input emoname
                for key in similars:
                    # Calculate the similarity
                    similars[key] = similarityBetween(key, emoname)
                    # Check if it contains the emoname
                    if emoname.lower() in key.lower():
                        suggestions.append(key)
                # Find the one(s) closest to the input emoname
                maxSimilarity = max([similars[key] for key in similars])
                # Take out their/its name
                for key in similars:
                    if similars[key] == maxSimilarity and key not in suggestions:
                        suggestions.append(key)
                # Build a suggestion string
                suggestionString = f"```Emoji not found: '{emoname}'.\nDid you mean: "
                # Append each suggestion into the string
                for i in range(0, len(suggestions)):
                    suggestionString += f"'{suggestions[i]}'"
                    if i != len(suggestions) - 1:
                        suggestionString += " or "
                suggestionString += "?```"
                # Send it
                log(suggestionString)
                await ctx.send(suggestionString)
            except Exception as e:
                eStr = f"```Error: {e.__repr__()}```"
                log(eStr)
                await ctx.send(eStr)

    # Send preview of emojis
    @commands.command()
    async def lsemo(self, ctx):
        if (re.search("Owner|Admin|Tech", str(ctx.author.roles))):
            await ctx.send("Emoji preview channel")
            for emoji in self.emojson:
                embed = discord.Embed()
                embed.title = emoji
                embed.set_image(url = self.emojson[emoji])
                await ctx.send(embed = embed)
        else:
            await ctx.send("```Only admins can do this.```")