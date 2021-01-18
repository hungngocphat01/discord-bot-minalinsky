# This file defines the SendHelpMsg module of the bot, including:

# Discord modules
import discord
from discord.ext import commands
# Main vars and funcs
from BasicDefinitions import runningOnHeroku, ver, date, startTime, startTimeStr, getTime, eventsdb, COMMAND_PREFIX
from Logging import *
import json

class SendHelpMsg(commands.Cog):
    COMMAND_PREFIX = "%"

    def __init__(self, bot):
        self.bot = bot
        log("Module loaded: SendHelpMsg")

    # Help command
    @commands.command(pass_context = True)
    async def help(self, ctx, cmd = None):
        command_log(ctx)
        j = json.loads(open("BotHelp.json", mode="rt").read())
        
        embed = discord.Embed()
        
        if (cmd is None):
            embed.title = f"Minalinsky v{ver}"
            embed.description = f"To get more information about a command, run `{COMMAND_PREFIX}help <command>`.\n`<arg>`: mandatory argument. `[arg]`: optional argument."
            for i in j:
                cmd = j[i]
                if cmd["args"] != 0:
                    args = " ".join(cmd["args"])
                else:
                    args = ""
                embed.add_field(name=COMMAND_PREFIX + i + " " + args, value=cmd["desc"], inline=False)
        else:
            if (cmd == "help"):
                embed.title = "Why call help command for the help command though?"
            elif (cmd not in j):
                embed.title = f"No such command: `{cmd}`"
            else:
                if j[cmd]["args"] != 0:
                    args = " ".join(j[cmd]["args"])
                else:
                    args = ""
                embed.title = cmd + " " + args
                embed.description = j[cmd]["desc"]
                if args != "":
                    for i in range(len(j[cmd]["args"])):
                        embed.add_field(name=j[cmd]["args"][i], value=j[cmd]["arg_desc"][i], inline=False)
                
                if "examples" in j[cmd]:
                    examples = ""
                    for i in range(len(j[cmd]["examples"])):
                        examples += j[cmd]["examples"][i] + "\n"
                    
                    embed.add_field(name="Examples", value=examples, inline=False)

        await ctx.send(embed=embed)
    # Help command
    @commands.command()
    async def changelog(self, ctx, cmd = None):
        command_log(ctx)
        changelogLines = open("changelog.txt").readlines()

        changelogContent = str()
        for line in changelogLines:
            changelogContent += line
        
        await ctx.send(f"```{changelogContent}```")
    
