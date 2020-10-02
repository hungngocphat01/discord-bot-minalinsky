# This file defines the SendHelpMsg module of the bot, including:

# Discord modules
import discord
from discord.ext import commands
# Main vars and funcs
from BasicDefinitions import runningOnHeroku, ver, date, startTime, startTimeStr, getTime, eventsdb, COMMAND_PREFIX


class SendHelpMsg(commands.Cog):
    COMMAND_PREFIX = "%"

    def __init__(self, bot):
        self.bot = bot
        print("Module loaded: SendHelpMsg")

    # Help command
    @commands.command(pass_context = True, aliases = ['event, ev'])
    async def help(self, ctx, cmd = None):
        print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")

        embed = discord.Embed()
        if (cmd is None):
            embed.title = f"**Minalinsky Bot v{ver}**"
            embedDesc = f"**Updated: {date}** \n\
**Command prefix:** {COMMAND_PREFIX} \n\n\
**Supported commands:** \n\
- `help`: shows this help message. \n\
- `time`: returns the current time in Vietnam. \n\
- `jptime`: returns the current time in Japan. \n\
- `time_at Etc/<timezone>`: returns the current time in the given timezone. \n\
Example: `%time_at Etc/GMT+9`. \n\n\
- `art`: send a number of images from Gelbooru.  \n\
- `hentai`: send a number of images from Gelbooru, but guaranteed to be nsfw. \n\
- `events`: returns a list of events in a given month.  \n\n\
**Special commands** \n\
- `shutdown` (bot owner): shutdowns the bot. \n\
- `restart` (everyone): disconnects the database and restarts the bot. \n\
- `purge <amount>` (admins only): deletes a given amount of messages in the current channel. \n\
- `evaluate <expression>`: evaluates a given expression. \n\
- `setrole <verb> <target_member> <role_name>`: give/delete a specific role to/from a specific member \n\
- `allroles <target_member> <command>`: give/delete all ``oshi`` roles to/from a specific member. \n\
- `premium <target_member> <command>`: give/delete premium membership to/from a specific member. \n\
- `query <expression>`: runs a query in the `eventsdb` table. The query string has to be in SQLite syntax. \n\
- `changelog`: as the name suggests. \n\n\
To show a command's help message, run `{COMMAND_PREFIX}help <command_name>`."
        else:
            embed.title = f"**Help for ``{cmd}`` command**"
            no_arg_cmd = ["time", "jptime", "shutdown"]
            builtin_arg_cmd = ["art", "hentai", "query"]

            if cmd == "help": 
                embedDesc = "What's the point of calling help on a help command?."
            elif cmd in no_arg_cmd:
                embedDesc = "This command has no argument."
            elif cmd == "time_at":
                embedDesc = "1 argument: the location at where time needs to be queried. Could be: \n\
- A location: ``Asia/Ho_Chi_Minh``, ``Asia/Tokyo``, ``Asia/Shanghai`` \n\
- A timezone: ``Etc/GMT+9``, ``Etc/GMT+7``, ..."
            elif cmd in builtin_arg_cmd:
                embedDesc = "Run the command without any argument to show its help message."
            elif cmd == "events":
                embedDesc = "Run without argument to query events within the current month.\n\
1 optional argument: month in which event list needs to be queried."
            elif cmd == "allroles":
                embedDesc = "[Admins only] 2 args:\n\
- A ``discord.Mention`` to the target member \n\
- Command keyword: ``give`` or ``delete``"
            elif cmd == "premium":
                embedDesc = "[Admins only] 2 args:\n\
- A ``discord.Mention`` to the target member \n\
- Command keyword: ``give`` or ``delete``"
            elif cmd == "setrole":
                embedDesc = "[Admins only] 3 args:\n\
- Command keyword: ``give`` or ``delete``\n\
- A ``discord.Mention`` to the target member \n\
- A string denoting the role's name (must be enclosed with quotes if white space char is present)."
            else:
                embedDesc = "Unknown command or this command does not include a help seperate message."

        embed.description = embedDesc
        embed.color = discord.Colour.orange()

        await ctx.send(embed = embed)
    # Help command
    @commands.command()
    async def changelog(self, ctx, cmd = None):
        changelogLines = open("changelog.txt").readlines()

        changelogContent = str()
        for line in changelogLines:
            changelogContent += line
        
        await ctx.send(f"```{changelogContent}```")
    
