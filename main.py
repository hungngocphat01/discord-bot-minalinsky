# Discord modules
import discord
from discord.ext import commands
# Supporting modules
import re
import traceback
from datetime import datetime
import mysql.connector
import pytz
# System modules
import platform 
import sys
import os

print("Bot started.")
#############  Read the database #############
try:
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "llevent",
        auth_plugin = "mysql_native_password"
    )
    sql = mydb.cursor()

    print("Database connected successfully.")
except Exception:
    print(f"Error: {traceback.print_exc()}")

def getTime(zone):
    now_utc = datetime.now(pytz.timezone("UTC"))
    now_zone = now_utc.astimezone(pytz.timezone(zone))
    return now_zone.strftime("%d/%m/%Y, %H:%M:%S")

def query(queryStr):
    try:
        sql.execute(queryStr)
        return sql.fetchall()
    except Exception as e:
        return repr(e)

#############  Init bot ############# 
TOKEN = "Njk0MTkxMTU5OTQ5MzkzOTgw.XqkGHQ.G_kobYaxKWpqSlTlVB3xEz-Unjw"

startTime = datetime.now()
startTimeStr = getTime("Asia/Ho_Chi_Minh")

ver = "0.1"
date = "30/04/2020"

bot = commands.Bot(command_prefix = "%")
bot.remove_command("help")

#############  Bot commands ############# 

# Purge messages command
@bot.command(pass_context = True)
async def purge(ctx, amount = 0):
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
@bot.command(pass_context = True)
async def evaluate(ctx, *, arg):
    print(f"{ctx.message.content} command called by {ctx.message.author}")
    if not re.search("import|open|def|sys|os", arg):
        try:
            await ctx.send(f"```{eval(arg)}```")
        except Exception as e:
            await ctx.send(f"```Error: {repr(e)}```")
    else: 
        await ctx.send("```Dangerous operation detected. Command execution cancelled.```")

# Shutdown command
@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    print(f"{ctx.message.content} command called by {ctx.message.author}")
    elapsedSecs = datetime.now() - startTime
    await ctx.send(f"""```Shutdown signal received. Shutting down. \nHad been running for {elapsedSecs}```""")
    await ctx.bot.logout()

# Test command
@bot.command()
async def test(ctx):
    print(f"{ctx.message.content} command called by {ctx.message.author}")
    await ctx.send("This is just a fucking test function.")

# Status command
@bot.command(pass_context = True)
async def status(ctx):
    print(f"{ctx.message.content} command called by {ctx.message.author}")
    statusString = f"""```markdown
Minalinsky v{ver}
Updated: {date}

Running on: {platform.system()} {platform.release()}
Started at: {startTimeStr} (Asia/Ho_Chi_Minh)
Current server: {ctx.guild}```"""
    await ctx.send(statusString)

# Help command
@bot.command(pass_context = True)
async def help(ctx):
    print(f"{ctx.message.content} command called by {ctx.message.author}")
    embedDesc = f"""**Updated: {date}**
Under development.
    
**Command prefix:** %
**Supported commands:**
`help`: shows this help message.
`time`: returns the current time in Vietnam.
`jptime`: returns the current time in Japan.
`time_at Etc/<timezone>`: returns the current time in the given timezone.
Example: `%time_at Etc/GMT+9`.

`events <month>`: returns a list of events in a given month. 
Constraint: 1 ≤ month ≤ 12.
Due to limitations regarding message length, all events within the year cannot be displayed at once.

**Special commands**
`addevent` (bot owner): add an event to the existing event list.
`shutdown` (bot owner): shutdown the bot.
`purge <amount>` (admins only): delete a given amount of messages in the current channel.
`evaluate <expression>`: evaluate a given expression.
`query <expression>`: run a query in the `llevent` database."""

    embed = discord.Embed()
    embed.title = f"**Minalinsky Bot v{ver}**"
    embed.description = embedDesc
    embed.color = discord.Colour.orange()

    await ctx.send(embed = embed)

# Say command
@bot.command(pass_context = True, aliases = ["s"])
async def say(ctx, *, arg):
    print(f"{ctx.message.content} command called by {ctx.message.author}")
    await ctx.send(arg)
    await ctx.message.delete()

# VN Time command
@bot.command(pass_context = True)
async def time(ctx):
    print(f"{ctx.message.content} command called by {ctx.message.author}")
    await ctx.send(f"```🇻🇳 Ima wa {getTime('Asia/Ho_Chi_Minh')} desu.```")

# JP Time command
@bot.command()
async def jptime(ctx):
    print(f"{ctx.message.content} command called by {ctx.message.author}")
    await ctx.send(f"```🇯🇵 Ima wa {getTime('Asia/Tokyo')} desu.```")

# Time as any timezone command
@bot.command()
async def time_at(ctx, arg = "UTC"):
    print(f"{ctx.message.content} command called by {ctx.message.author}")
    if arg == "list":
        for i in pytz.common_timezones:
            await ctx.send(f"```{i}```")
        await ctx.send(f"```{len(pytz.common_timezones)} timezones listed```")
    else: 
        await ctx.send(f"```Ima, {arg} de wa {getTime(arg)} desu.```")

# Get all events in a given month
@bot.command()
async def events(ctx, month = datetime.now().month):
    try:
        queryStr = f"select * from events where extract(month from date) = {month}"
        print(f"Query called by: {ctx.message.author}\n{queryStr}")
        queryResult = query(queryStr)
        
        resultMessage = f"```md\nEvents list in Month {month}\nQuery string: {queryStr}\n\n"

        longestDetailStr = str(max([len(record[2]) for record in queryResult]))
        longestNoteStr = str(max([len(record[3]) for record in queryResult]))

        for record in queryResult:
            fmtString = ("{:2}  {:2}  {:" + longestDetailStr +  "}  {:" + longestNoteStr + "}\n").format(record[0].day, record[1], record[2], record[3])
            resultMessage += fmtString
        resultMessage += "```"
        await ctx.send(resultMessage)       
    except Exception:
        eStr = f"{traceback.print_exc()}"
        print(eStr)
        await ctx.send(f"```{eStr}```")

############# Bot events ############# 
@bot.event
async def on_ready():
    print("Bot ready.")

@bot.event
async def on_message(message):
    triggered = False
    try:
        # Hello
        if "hello" in message.content.lower():
            await message.channel.send(f"Okarinasai, {message.author.name}-sama!")
            triggered = True
        # Chào mọi người
        elif "chào mọi người" in message.content.lower():
            await message.channel.send("Hajimemashite, watashi wa Minalinsky, Honoka-chan no nha tien tri vu tru ya co van toi cao desu!")
            await message.channel.send("Korekara wa yoroshiku ne!")
            triggered = True
        # Good night
        elif (re.search("g9|night|good|oyasumi|ngủ", message.content.lower())) and (message.author.id != bot.user.id) and ("say" not in message.content.lower()):
            await message.channel.send("Oyasuminasaiiiii~")
            triggered = True
        # Bye
        elif "bye" in message.content.lower():
            await message.channel.send(f"Mata ne~~")
            triggered = True
        # DCSVN
        elif "đảng" in message.content.lower():
            await message.channel.send("<:dang:694251236895227965> "*3)
            triggered = True
        if (triggered): 
            print(f"Message triggered: \"{message.content}\", Channel: #{message.channel.name}")

    except Exception as e:
        await message.channel.send(f"```Error: {e}```Honoka-chaaaaaan. Mite mite~")

    await bot.process_commands(message)

############# Run bot ############# 
bot.run(TOKEN) 