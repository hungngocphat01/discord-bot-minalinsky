import discord
from discord.ext import commands
import copy
import re
from BasicDefinitions import emojson, similarityBetween, COMMAND_PREFIX

class Emoji(commands.Cog):
    def __init__(self, bot):
        print("Module loaded: Emoji")
        self.bot = bot

    # Send emoji
    @commands.command(aliases = ["emo"])
    async def emoji(self, ctx, emoname = None):
        print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
        if emoname == None:
            helpStr = f"""```Usage:
{COMMAND_PREFIX}emoji list: list all emoji names (text only).
{COMMAND_PREFIX}emoji <name>: send an emoji with given name.

    For preview of emojis, go to channel #usable-emoji```"""
            await ctx.send(helpStr)
        elif emoname.lower() == "list":
            emojilistStr = f"```Emoji list:\n\n"
            for key in emojson:
                emojilistStr += str(key) + "\n"
            emojilistStr += "```"
            await ctx.send(emojilistStr)
        else:
            print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
            try:
                embed = discord.Embed()
                embed.set_author(name = ctx.message.author.display_name, icon_url = ctx.message.author.avatar_url)
                embed.set_image(url = str(emojson[emoname]))
                await ctx.message.delete()
                await ctx.send(embed = embed)        
            except KeyError:
                suggestions = []
                # Copy the emojson dictionary
                similars = copy.deepcopy(emojson)
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
                print(suggestionString)
                await ctx.send(suggestionString)
            except Exception as e:
                eStr = f"```Error: {e.__repr__()}```"
                print(eStr)
                await ctx.send(eStr)

    # Send preview of emojis
    @commands.command()
    async def lsemo(self, ctx):
        if (re.search("Owner|Admin|Tech", str(ctx.author.roles))):
            await ctx.send("Emoji preview channel")
            for emoji in emojson:
                embed = discord.Embed()
                embed.title = emoji
                embed.set_image(url = emojson[emoji])
                await ctx.send(embed = embed)
        else:
            await ctx.send("```Only admins can do this.```")