# This file defines the BasicCommands of the bot, including:
#   purge
#   eval
#   shutdown
#   restart
#   status
#   help
#   say
#   time, jptime, time_at
#   gem

# Discord modules
import discord
from discord.ext import commands
# Support modules
import re
from datetime import datetime
import platform
import pytz
# Main vars and funcs
from BasicDefinitions import runningOnHeroku, ver, date, startTime, startTimeStr, getTime, eventsdb, COMMAND_PREFIX

class BasicCommands(commands.Cog):
    COMMAND_PREFIX = "%"

    def __init__(self, bot):
        self.bot = bot
    # Purge messages command
    @commands.command(pass_context = True)
    async def purge(self, ctx, amount = 0):
        if (re.search("Owner|Admin|Tech", str(ctx.author.roles))):
            if amount > 0:
                await ctx.channel.purge(limit = amount)
                await ctx.send(f"```🗑️ {amount} meseeji wo keshimashita~```")
            elif amount == 0:
                await ctx.send("J xoá 0 tin nhắn là xoá thế nào.")
            else:
                await ctx.send("J số đếm mà âm được à. Về học lại lớp 1 đi.")
            print(f"Purged {amount} message(s) from {ctx.message.channel}, called by {ctx.message.author}")
        else:
            await ctx.send("J chỉ có admin mới được dùng lệnh này thôi.")

    # Evaluate command
    @commands.command(pass_context = True, aliases = ["eval"])
    async def evaluate(self, ctx, *, arg):
        print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
        if (not re.search("import|open|def|sys|os", arg)) or ("owner" in ctx.message.author.lower()):
            try:
                await ctx.send(f"```{eval(arg)}```")
            except Exception as e:
                await ctx.send(f"```Error: {repr(e)}```")
        else: 
            await ctx.send("```Dangerous operation detected. Command execution cancelled.```")

    # Shutdown command
    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
        elapsedSecs = datetime.now() - startTime
        await ctx.send(f"""```Shutdown signal received. Shutting down. \nHad been running for {elapsedSecs}```""")
        await ctx.bot.logout()

    # Restart command
    @commands.command()
    @commands.is_owner()
    async def restart(self, ctx):
        print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
        if runningOnHeroku:
            elapsedSecs = datetime.now() - startTime
            await ctx.send(f"""```Restarting...\nHad been running for {elapsedSecs}```""")
            await ctx.bot.logout()
        else:
            await ctx.send(f"""```Restart command can only be used if the bot is running on Heroku.```""")


    # Status command
    @commands.command(pass_context = True)
    async def status(self, ctx):
        print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
        statusString = f"""```markdown
Minalinsky v{ver}
Updated: {date}

Running on: {platform.system()} {platform.release()}
Heroku: {runningOnHeroku}
Started at: {startTimeStr} (Asia/Ho_Chi_Minh)
Current server: {ctx.guild}
Database connected: {eventsdb is not None}```"""
        await ctx.send(statusString)

    # Help command
    @commands.command(pass_context = True, aliases = ['event, ev'])
    async def help(self, ctx):
        print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
        embedDesc = f"""**Updated: {date}**
        
**Command prefix:** {COMMAND_PREFIX}
**Supported commands:**
- `help`: shows this help message.
- `time`: returns the current time in Vietnam.
- `jptime`: returns the current time in Japan.
- `time_at Etc/<timezone>`: returns the current time in the given timezone.
Example: `%time_at Etc/GMT+9`.
- `art`: send a number of images from Gelbooru (a Danbooru alternative). 
Type ``{COMMAND_PREFIX}art`` for more information.

- `events <month> [full]`: returns a list of events in a given month. 
Constraint: `1 ≤ month ≤ 12`.
Due to limitations regarding message length, all events within the year cannot be displayed at once.
`full`: display note in full form
**Warning:** can be improperly displayed in portrait mode (on mobile phones, etc).

**Special commands**
- `shutdown` (bot owner): shutdowns the bot.
- `restart` (everyone): disconnects the database and restarts the bot.
- `purge <amount>` (admins only): deletes a given amount of messages in the current channel.
- `evaluate <expression>`: evaluates a given expression.
- `query <expression>`: runs a query in the `lleventdb` table. The query string have to be in SQLite syntax."""

        embed = discord.Embed()
        embed.title = f"**Minalinsky Bot v{ver}**"
        embed.description = embedDesc
        embed.color = discord.Colour.orange()

        await ctx.send(embed = embed)

    # Say command
    @commands.command(pass_context = True, aliases = ["s"])
    async def say(self, ctx, *, arg):
        print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
        await ctx.message.delete()
        await ctx.send(arg)

    # VN Time command
    @commands.command(pass_context = True)
    async def time(self, ctx):
        print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
        await ctx.send(f"```python\n🇻🇳 Ima wa {getTime('Asia/Ho_Chi_Minh')} desu.```")

    # JP Time command
    @commands.command()
    async def jptime(self, ctx):
        print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
        await ctx.send(f"```python\n🇯🇵 Ima wa {getTime('Asia/Tokyo')} desu.```")

    # Time as any timezone command
    @commands.command()
    async def time_at(self, ctx, arg = "UTC"):
        print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
        if arg == "list":
            for i in pytz.common_timezones:
                await ctx.send(f"```{i}```")
            await ctx.send(f"```{len(pytz.common_timezones)} timezones listed```")
        else: 
            await ctx.send(f"```python\nIma, {arg} de wa {getTime(arg)} desu.```")

    @commands.command()
    async def gem(self, ctx):
        print(f"\n'{ctx.message.content}' command ca    lled by {ctx.message.author}")
        rates = [[86, 48.13], [50, 28.66], [26, 16.11], [12, 8.05], [5, 3.46], [1, 1.12]]
        n_price = 0
        n_quantity = int(ctx.message.content)
        QUANTITY = 0
        PRICE = 1
        while n_quantity != 0:
            for rate in rates:
                if rate[QUANTITY] <= n_quantity:
                    n_price += rate[PRICE]
                    n_quantity -= rate[QUANTITY]
                    break
        await ctx.send(f"```{ctx.message.content} equals to {n_price} USD or {n_price * 23400} VND```")

