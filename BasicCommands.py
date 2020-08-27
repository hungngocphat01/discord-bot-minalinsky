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
        print("Module loaded: BasicCommands")
    
    # Purge messages command
    @commands.command(pass_context = True)
    async def purge(self, ctx, amount = 0):
        if (re.search("Owner|Admin|Tech", str(ctx.author.roles))):
            if amount > 0:
                await ctx.channel.purge(limit = amount + 1)
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

    @commands.command()
    async def stats(self, ctx):
        print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
        if (ctx.guild is not None):
            guild = ctx.guild
            bot_num, online_num = 0, 0
            for mem in guild.members:
                if (mem.bot):
                    bot_num += 1
                elif (mem.status != discord.Status.offline):
                    online_num += 1
            
            stats  = "```Guild information report\n\n"
            stats += f"Guild name: {guild.name}\n"
            stats += f"Region: {guild.region}\n"
            stats += f"Text channels: {len(guild.text_channels)}\n"
            stats += f"Members: {len(guild.members)}\n"
            stats += f"Online: {online_num}, Bots: {bot_num}\n"
            stats += f"Owner: {guild.owner.display_name}\n"
            stats += f"Boosters: {[m.display_name for m in guild.premium_subscribers]}\n"
            stats += "```"
            await ctx.send(stats)

    @commands.command()
    async def whois(self, ctx):
        print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
        mem = ctx.message.mentions[0]

        if (mem is not None):
            embed = discord.Embed(color=mem.color)
            embed.title = "Member information"
            embed.set_image(url = mem.avatar_url)
            embed.add_field(
                name = "Name",
                value = str(mem),
                inline = True
            )
            embed.add_field(
                name = "Display name",
                value = mem.display_name,
                inline = True
            )
            embed.add_field(
                name = "Joined on",
                value = mem.joined_at.strftime("%d-%m-%Y"),
                inline = False

            )
            embed.add_field(
                name = "Booster",
                value = mem.premium_since.strftime("%d-%m-%Y") if mem.premium_since is not None else "No",
                inline = True
            )
            embed.add_field(
                name = "Status",
                value = "Offine" if mem.status == discord.Status.offline else "Online",
                inline = True
            )
            embed.add_field(
                name = "Roles",
                value = [role.name for role in mem.roles if role.name != "@everyone"],
                inline = False
            )
            if (mem.activity is not None):
                embed.add_field(
                    name = "Currently " + \
                    ("playing" if mem.activity.type == discord.ActivityType.playing \
                    else "watching" if mem.activity.type == discord.ActivityType.watching \
                    else "listening" if mem.activity.type == discord.ActivityType.listening \
                    else "watching" if mem.activity.type == discord.ActivityType.watching \
                    else "playing" if mem.activity.type == discord.ActivityType.playing \
                    else "streaming" if mem.activity.type == discord.ActivityType.streaming \
                    else "doing something with") + " " + mem.activity.name,
                    value = mem.activity.details,
                    inline = False
                )
            await ctx.send(embed=embed)
        else:
            await ctx.send("```Error: Cannot get member from mention```")

    # Restart command
    @commands.command()
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
    async def gem(self, ctx, arg):
        print(f"\n'{ctx.message.content}' command ca    lled by {ctx.message.author}")
        rates = [[86, 48.13], [50, 28.66], [26, 16.11], [12, 8.05], [5, 3.46], [1, 1.12]]
        n_price = 0
        n_quantity = int(arg)
        QUANTITY = 0
        PRICE = 1
        while n_quantity != 0:
            for rate in rates:
                if rate[QUANTITY] <= n_quantity:
                    n_price += rate[PRICE]
                    n_quantity -= rate[QUANTITY]
                    break
        await ctx.send(f"```{arg} gems equals to approx. {round(n_price, 2)} USD or {int(n_price * 23400)} VND```")

