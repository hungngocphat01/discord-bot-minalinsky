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
from discord import message
from discord.ext.commands.core import Command
from Administration import is_admin
import discord
from discord.ext import commands
# Support modules
import re
from datetime import datetime
import platform
import pytz
import math
# Main vars and funcs
from BasicDefinitions import runningOnHeroku, ver, date, startTime, startTimeStr, getTime, COMMAND_PREFIX
from EventQuery import session
from Logging import *

class BasicCommands(commands.Cog):
    COMMAND_PREFIX = "%"

    def __init__(self, bot):
        self.bot = bot
        log("Module loaded: BasicCommands")
    
    # Purge messages command
    @commands.command(pass_context = True)
    async def purge(self, ctx, amount = 0):
        command_log(ctx)
        if (is_admin(ctx.author.top_role.id)):
            if amount > 0:
                await ctx.channel.purge(limit = amount + 1)
                await ctx.send(f"```🗑️ {amount} meseeji wo keshimashita~```")
            elif amount == 0:
                await ctx.send("J xoá 0 tin nhắn là xoá thế nào.")
            else:
                await ctx.send("J số đếm mà âm được à. Về học lại lớp 1 đi.")
            log(f"Purged {amount} message(s) from {ctx.message.channel}, called by {ctx.message.author}")
        else:
            await ctx.send("J chỉ có admin mới được dùng lệnh này thôi.")

    # Evaluate command
    @commands.command(pass_context = True, aliases = ["eval"])
    async def evaluate(self, ctx, *, arg):
        command_log(ctx)
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
        command_log(ctx)  
        elapsedSecs = datetime.now() - startTime
        await ctx.send(f"""```Shutdown signal received. Shutting down. \nHad been running for {elapsedSecs}```""")
        await ctx.bot.logout()

    # Restart command
    @commands.command()
    async def restart(self, ctx):
        command_log(ctx)
        if runningOnHeroku:
            elapsedSecs = datetime.now() - startTime
            await ctx.send(f"""```Restarting...\nHad been running for {elapsedSecs}```""")
            await ctx.bot.logout()
        else:
            await ctx.send(f"""```Restart command can only be used if the bot is running on Heroku.```""")


    # Status command
    @commands.command(pass_context = True)
    async def status(self, ctx):
        command_log(ctx)  
        statusString = f"""```md
Minalinsky v{ver}
By Hung Ngoc Phat
Updated: {date}

Running on: {platform.system()} {platform.release()}
Heroku: {runningOnHeroku}
Started at: {startTimeStr} (Asia/Ho_Chi_Minh)
Current server: {ctx.guild}
SQLAlchemy session: {session.is_active}```"""
        await ctx.send(statusString)

    # Say command
    @commands.command(pass_context = True, aliases = ["s"])
    async def say(self, ctx, *, arg):
        command_log(ctx)
        await ctx.message.delete()
        if (not is_admin(ctx.author.top_role.id)):
            log("Tagging in say command for non-admins is prohibited.")
            arg = arg.replace("@", "`@`")
        await ctx.send(arg)

    # VN Time command
    @commands.command(pass_context = True)
    async def time(self, ctx):
        command_log(ctx)
        await ctx.send(f"```python\n🇻🇳 Ima wa {getTime('Asia/Ho_Chi_Minh')} desu.```")

    # JP Time command
    @commands.command()
    async def jptime(self, ctx):
        command_log(ctx)
        await ctx.send(f"```python\n🇯🇵 Ima wa {getTime('Asia/Tokyo')} desu.```")

    # Time as any timezone command
    @commands.command()
    async def time_at(self, ctx, arg = "UTC"):
        command_log(ctx)  
        if arg == "list":
            for i in pytz.common_timezones:
                await ctx.send(f"```{i}```")
            await ctx.send(f"```{len(pytz.common_timezones)} timezones listed```")
        else: 
            await ctx.send(f"```python\nIma, {arg} de wa {getTime(arg)} desu.```")

    # Convert gem into $$$
    @commands.command()
    async def gem(self, ctx, arg):
        command_log(ctx)
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
    
    @commands.command()
    async def khabanh(self, ctx, *, arg):
        command_log(ctx)
        if len(arg) != 0:
            words = arg.split()
            result = []
            for i in range(0, len(words)):
                newword = ""
                for j in range(0, len(words[i])):
                    newword += words[i][j].lower() if j % 2 == 0 else words[i][j].upper()
                result.append(newword)
            embed = discord.Embed()
            embed.set_author(name = ctx.message.author.display_name, icon_url = ctx.message.author.avatar_url)
            embed.description = " ".join(result)

            await ctx.message.delete()
            await ctx.send(embed = embed)

    @commands.command()
    async def stats(self, ctx):
        command_log(ctx)
        embed = discord.Embed()

        embed.set_author(name = ctx.guild.name, icon_url = ctx.guild.icon_url)
        members = ctx.guild.members
        contributed_members = " ".join([x.mention for x in ctx.guild.premium_subscribers if x is not None])

        embed.add_field(name = "Channels", value = len(ctx.guild.channels), inline=True)
        embed.add_field(name = "Members", value = len(members), inline=True)
        embed.add_field(name = "Online members (non-bot)", value = len([x for x in members if (x.status is not discord.Status.offline) and (x.status is not discord.Status.invisible) and (not x.bot)]), inline=False)
        embed.add_field(name = "Bots", value=len([x for x in members if x.bot]), inline=True)
        embed.add_field(name = "Contributors", value = contributed_members, inline=False)
        embed.add_field(name = "Boost Level", value = ctx.guild.premium_tier, inline=True)
        embed.add_field(name = "Boost Number", value = ctx.guild.premium_subscription_count, inline=True)
        embed.add_field(name = "Owner", value = ctx.guild.get_member(ctx.guild.owner_id).mention, inline=False)
        embed.set_image(url = ctx.guild.icon_url)
        
        await ctx.send(embed = embed)

    @commands.command()
    async def journalctl(self, ctx, num=None):
        command_log(ctx)  
        arid = ctx.message.author.top_role.id

        if (not is_admin(arid)):
            e = f"{ctx.message.author} does not have sufficient permission to invoke this command."
            log(e)
            await ctx.send(f"```{e}```")
            return

        if num is not None:
            num = int(num)
            if (num == 0):
                log("Number of messages must be non-zero.")
                return
            elif (num < 0):
                logmsg = "\n".join(runtime_logs[None:(-1)*num])
            elif (num > 0):
                begin_index = len(runtime_logs) - num
                if (begin_index < 0):
                    begin_index = 0
                logmsg = "\n".join(runtime_logs[begin_index:None])
        else:
            logmsg = "\n".join(runtime_logs)

        if (len(logmsg) > 2000):
            logmsg = log[len(logmsg)-1980:None]
            logmsg = "(Truncated)...\n" + log

        await ctx.send(f"```css\n{logmsg}```")
    
    @commands.command()
    async def addemoji(self, ctx, msg, emoji):
        command_log(ctx)
        e = [x for x in ctx.guild.emojis if x.name == emoji]
        if (len(e) > 0):
            e = e[0]
            messages = [m for m in await ctx.channel.history(limit=50).flatten() if m != ctx.message]
            for m in messages:
                if msg in m.content:
                    await m.add_reaction(e)
                    await ctx.message.delete()
                    return
