# Discord modules
import discord
from discord.ext import commands
# Supporting modules
import re
import traceback
from datetime import datetime
import pytz
import json
import copy

# Database simulation libraries
import pandas as pd
import pandasql
from tabulate import tabulate

# System modules
import platform 
import sys
import os

ver = "2.0 beta"
date = "02/05/2020"
runningOnHeroku = (os.getenv("RUNNING_ON_HEROKU") == "1")
print("Bot started.")

#############  Read the database #############
# Import database
eventsdb = None

try:
    eventsdb = pd.read_excel("events.xlsx")
except FileNotFoundError:
    print("Database file not found. Please check again.")

# Init pandasql
pquery = lambda queryStr: pandasql.sqldf(queryStr, globals())
query = lambda queryStr: tabulate(pquery(queryStr), showindex = False, headers = [])

# Read the emoji.json
emojson = json.load(open("emoji.json"))

def getTime(zone):
    now_utc = datetime.now(pytz.timezone("UTC"))
    now_zone = now_utc.astimezone(pytz.timezone(zone))
    return now_zone.strftime("%d/%m/%Y, %H:%M:%S")

def differenceBetween(str1, str2):
    diff = 0
    if len(str1) > len(str2):
        for char1 in str1:
            for char2 in str2:
                if char1 != char2: diff += 1
    else:
        for char2 in str2:
            for char1 in str1:
                if char1 != char2: diff += 1
    return diff

#############  Init bot ############# 
TOKEN = "Njk0MTkxMTU5OTQ5MzkzOTgw.XqkGHQ.G_kobYaxKWpqSlTlVB3xEz-Unjw"

startTime = datetime.now()
startTimeStr = getTime("Asia/Ho_Chi_Minh")

if runningOnHeroku:
    COMMAND_PREFIX = "%"
else:
    COMMAND_PREFIX = "&"

bot = commands.Bot(command_prefix = COMMAND_PREFIX)

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
@bot.command(pass_context = True, aliases = ["eval"])
async def evaluate(ctx, *, arg):
    print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
    if (not re.search("import|open|def|sys|os", arg)) or ("owner" in ctx.message.author.lower()):
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
    print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
    elapsedSecs = datetime.now() - startTime
    await ctx.send(f"""```Shutdown signal received. Shutting down. \nHad been running for {elapsedSecs}```""")
    await ctx.bot.logout()

# Restart command
@bot.command()
@commands.is_owner()
async def restart(ctx):
    print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
    if runningOnHeroku:
        elapsedSecs = datetime.now() - startTime
        await ctx.send(f"""```Restarting...\nHad been running for {elapsedSecs}```""")
        await ctx.bot.logout()
    else:
        await ctx.send(f"""```Restart command can only be used if the bot is running on Heroku.```""")

# Test command
@bot.command()
async def emoji(ctx, emoname):
    print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
    try:
        embed = discord.Embed()
        embed.title = f"Emoji requested by {ctx.message.author}"
        embed.set_image(url = str(emojson[emoname]))
        await ctx.send(embed = embed)
    except KeyError:
        # Copy the emojson dictionary
        diffs = copy.deepcopy(emojson)
        # With each emoji, find the difference between its name and the input emoname
        for key in diffs:
            diffs[key] = differenceBetween(key, emoname)
        # Find the one(s) closest to the input emoname
        smallestDiff = min([diffs[key] for key in diffs])
        # Take out their/its name
        suggestions = [key for key in diffs if diffs[key] == smallestDiff]
        # Build a suggestion string
        suggestionString = f"```Emoji not found: '{emoname}'.\nDo you mean: "
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


# Status command
@bot.command(pass_context = True)
async def status(ctx):
    print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
    statusString = f"""```markdown
Minalinsky v{ver}
Updated: {date}

Running on: {platform.system()} {platform.release()}
Heroku: {runningOnHeroku}
Started at: {startTimeStr} (Asia/Ho_Chi_Minh)
Current server: {ctx.guild}
Database connected: {eventsdb != None}```"""
    await ctx.send(statusString)

# Help command
@bot.command(pass_context = True, aliases = ['event, ev'])
async def help(ctx):
    print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
    embedDesc = f"""**Updated: {date}**
Under development.
    
**Command prefix:** {COMMAND_PREFIX}
**Supported commands:**
- `help`: shows this help message.
- `time`: returns the current time in Vietnam.
- `jptime`: returns the current time in Japan.
- `time_at Etc/<timezone>`: returns the current time in the given timezone.
Example: `%time_at Etc/GMT+9`.

- `events <month> [full]`: returns a list of events in a given month. 
Constraint: `1 ≤ month ≤ 12`.
Due to limitations regarding message length, all events within the year cannot be displayed at once.
- `full`: display note in full form
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
@bot.command(pass_context = True, aliases = ["s"])
async def say(ctx, *, arg):
    print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
    await ctx.message.delete()
    await ctx.send(arg)

# VN Time command
@bot.command(pass_context = True)
async def time(ctx):
    print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
    await ctx.send(f"```python\n🇻🇳 Ima wa {getTime('Asia/Ho_Chi_Minh')} desu.```")

# JP Time command
@bot.command()
async def jptime(ctx):
    print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
    await ctx.send(f"```python\n🇯🇵 Ima wa {getTime('Asia/Tokyo')} desu.```")

# Time as any timezone command
@bot.command()
async def time_at(ctx, arg = "UTC"):
    print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
    if arg == "list":
        for i in pytz.common_timezones:
            await ctx.send(f"```{i}```")
        await ctx.send(f"```{len(pytz.common_timezones)} timezones listed```")
    else: 
        await ctx.send(f"```python\nIma, {arg} de wa {getTime(arg)} desu.```")

# Query command
@bot.command(aliases = ["query"])
async def botquery(ctx, queryStr = None):
    print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
    if queryStr != None:
        try:
            queryResult = "```css\nQuery result: \n\n"
            queryResult += query(queryStr) + "```"
            print(queryResult)
            await ctx.send(queryResult)
        except Exception as e:
            eStr = f"Error: {e.__repr__()}"
            print(eStr)
            await ctx.send(eStr)
    else:
        print("No query string detected.")
        await ctx.send(f"""```python
Query command usage:
{COMMAND_PREFIX}query "<sql_query_string>" (with quote)

Query string have to be in SQLite syntax.
The table name is EVENTSDB.
The year in the DATE field of all records is 2010.
There are 4 fields in the EVENTS table:
- DATE: event date, stored in datetime format. To specify the format, use something like: "select strftime(date, "%d-%m") as date, ..."
- TYPE ('BD' = 'Birthday', 'AN' = 'Anime Episode that has an Insert song', 'RE': 'Release of an important single or PV', 'SP': 'Special events')
- DETAILS: the detail of the event.
- NOTE: Note of the event. Abbreviated to optimize displaying on mobile phones.
- FULLNOTE: Note of the event. Not abbreviated.

Ex: {COMMAND_PREFIX}query "select * from events where date > '2010-4-1'"```""")

# Query events in a month
@bot.command()
async def events(ctx, month = None, full = None):
    try:
        if (str(month).lower() == "full"):
            month = datetime.now().month
            full = "full"
        elif (month == None):
            month = datetime.now().month

        monthName = datetime(2020, int(month), 1).strftime("%B")

        await ctx.send(f"List of events in {monthName}:")
        if (full == None):
            await botquery(ctx, f"select strftime('%d', date) as day, type, details, note from eventsdb where cast(strftime('%m', date) as integer) = {month}")
        elif (full.lower() == "full"):
            await botquery(ctx, f"select strftime('%d', date) as day, type, details, fullnote from eventsdb where cast(strftime('%m', date) as integer) = {month}")
    except Exception as e:
        await ctx.send(f"``Error: {e}``")
        print(f"\nError: {e}")

# Query the next event
@bot.command()
async def nextev(ctx):
    print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
    currentDate = datetime.now().strftime("2010-%m-%d")
    events = pquery(f"select * from eventsdb where date = (select date from eventsdb where date > '{currentDate}' limit 1)").values.tolist()
    print(events)
    eventNo = 1
    eventTypes = {"BD": "Birthday", "AN": "Anime Episode with Insert Song", "RE": "Release", "SP": "Special", "PV": "PV"}

    if (len(events) == 0):
        await ctx.send("The previous event is the final one within this year. See you again next year :penguin: ")
    if (len(events) > 1):
        await ctx.send("Next events:")

    for event in events:
        embed = discord.Embed()
        if (len(events) > 1):
            embed.title = f"Event {eventNo}"
            eventNo += 1
        else:
            embed.title = f"Next event"

        embed.add_field(name = "Date",
            value = str(event[0].split("-")[2].split(" ")[0]) + "/" + str(event[0].split("-")[1]),
            inline = False
        )
        embed.add_field(
            name = "Type",
            value = eventTypes[event[1]],
            inline = False
        )
        embed.add_field(
            name = "Details",
            value = event[2], 
            inline = True
        )
        embed.add_field(
            name = "Note",
            value = event[4],
            inline = True
        )

        embed.color = discord.Colour.orange()
        await ctx.send(embed = embed)  
                 
############# Bot events ############# 
@bot.event
async def on_ready():
    print("Bot ready.")

@bot.event
async def on_message(message):
    triggered = False
    try:
        if "say" not in message.content:
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
            elif (re.search("g9|night|good|oyasumi|ngủ", message.content.lower())) and (message.author.id != bot.user.id):
                await message.channel.send("Oyasuminasaiiiii~")
                triggered = True
            # Bye
            elif "bye" in message.content.lower():
                await message.channel.send(f"Mata ne~~")
                triggered = True
            # DCSVN
            elif re.match("đảng|đcs|cộng sản|vn|việt nam|vietnam", message.content.lower()):
                await message.channel.send("<:dang:694251236895227965> "*3)
                triggered = True
            if (triggered): 
                print(f"\nMessage triggered: \"{message.content}\", Channel: #{message.channel.name}")

    except Exception as e:
        await message.channel.send(f"```Error: {e}```Honoka-chaaaaaan. Mite mite~")

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        print(f"\nUnexisting '{ctx.message.content}' command called by {ctx.message.author}")
        await ctx.send(f"```Command not found: {ctx.message.content.split()[0]} ```")
    raise error

############# Run bot #############
try:
    bot.run(TOKEN)
except:
    print("Bot stopped working.")