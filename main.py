# Discord modules
import discord
from discord.ext import commands
# Supporting modules
import re
import traceback
from datetime import datetime
import psycopg2
import pytz
# System modules
import platform 
import sys
import os

print("Bot started.")
#############  Read the database on local #############
try:
    mydb = psycopg2.connect(
        host = "localhost",
        user = "ngocphat",
        password = "3388",
        database = "llevent"
    )
    sql = mydb.cursor()

    print("Database connected successfully.")
    dbConnected = True
except Exception:
    print(f"Error: {traceback.print_exc()}")
    dbConnected = False
#############  Read the database on Heroku #############
# try:
#     DATABASE_URL = os.environ['DATABASE_URL']
#     mydb = psycopg2.connect(DATABASE_URL, sslmode='require')
#     sql = mydb.cursor()

#     print("Database connected successfully.")
#     dbConnected = True
# except Exception:
#     print(f"Error: {traceback.print_exc()}")
#     dbConnected = False

def getTime(zone):
    now_utc = datetime.now(pytz.timezone("UTC"))
    now_zone = now_utc.astimezone(pytz.timezone(zone))
    return now_zone.strftime("%d/%m/%Y, %H:%M:%S")

def query(queryStr):
    try:
        sql.execute(queryStr)
        mydb.commit()
        return sql.fetchall()
    except Exception as e:
        return repr(e)

#############  Init bot ############# 
TOKEN = "Njk0MTkxMTU5OTQ5MzkzOTgw.XqkGHQ.G_kobYaxKWpqSlTlVB3xEz-Unjw"

startTime = datetime.now()
startTimeStr = getTime("Asia/Ho_Chi_Minh")

ver = "1.0"
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
@bot.command(pass_context = True, aliases = ["eval"])
async def evaluate(ctx, *, arg):
    print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
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
    print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
    elapsedSecs = datetime.now() - startTime
    await ctx.send(f"""```Shutdown signal received. Shutting down. \nHad been running for {elapsedSecs}```""")
    await ctx.bot.logout()

# Test command
@bot.command()
async def test(ctx):
    print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
    await ctx.send("This is just a fucking test function.")

# Status command
@bot.command(pass_context = True)
async def status(ctx):
    print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
    statusString = f"""```markdown
Minalinsky v{ver}
Updated: {date}

Running on: {platform.system()} {platform.release()}
Started at: {startTimeStr} (Asia/Ho_Chi_Minh)
Current server: {ctx.guild}
Database connected: {dbConnected}```"""
    await ctx.send(statusString)

# Help command
@bot.command(pass_context = True, aliases = ['event, ev'])
async def help(ctx):
    print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
    embedDesc = f"""**Updated: {date}**
Under development.
    
**Command prefix:** %
**Supported commands:**
`help`: shows this help message.
`time`: returns the current time in Vietnam.
`jptime`: returns the current time in Japan.
`time_at Etc/<timezone>`: returns the current time in the given timezone.
Example: `%time_at Etc/GMT+9`.

`events <month> [full]`: returns a list of events in a given month. 
Constraint: 1 ≤ month ≤ 12.
Due to limitations regarding message length, all events within the year cannot be displayed at once.
[full]: display note in full form
**Warning:** can be improperly displayed in portrait mode (on mobile phones, etc).

**Special commands**
`addevent` (bot owner): add an event to the existing event list.
`shutdown` (bot owner): shutdown the bot.
`purge <amount>` (admins only): delete a given amount of messages in the current channel.
`evaluate <expression>`: evaluate a given expression.
`query <expression>`: run a query in the `llevent` database. The query string MUST begin with 'select'
`sudoquery <expression> (owner only): run a query in the `llevent` database without any restrictions."""

    embed = discord.Embed()
    embed.title = f"**Minalinsky Bot v{ver}**"
    embed.description = embedDesc
    embed.color = discord.Colour.orange()

    await ctx.send(embed = embed)

# Say command
@bot.command(pass_context = True, aliases = ["s"])
async def say(ctx, *, arg):
    print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
    await ctx.send(arg)
    await ctx.message.delete()

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
async def botquery(ctx, queryStr = None, calledFromMonthFunc = False):
    if queryStr != None:
        if (queryStr.lower().lstrip().startswith("select")):
            try:
                queryResult = query(queryStr)
                if dbConnected:
                    print(f"\nQuery called by: {ctx.message.author}\n{queryStr}")
                    print(queryResult)
                    resultMessage = f"```python\nQuery result:\n\n"
                    longestLength = []
                    if type(queryResult) is list: 
                        # Calculating longest record of each column
                        for columnNo in range(0, len(queryResult[0])):
                            array = [len(str(record[columnNo])) for record in queryResult]
                            longestLength.append(str(max(array)))
                        # Appending result to resultMessage
                        for record in queryResult:
                            # Read each column in current record
                            for columnNo in range(0, len(record)):
                                # Append current column
                                resultMessage += ("{:" + longestLength[columnNo] + "}").format(str(record[columnNo]))
                                # 2 spaces or new line?
                                if columnNo < len(record) - 1:
                                    resultMessage += "  "
                                else:
                                    resultMessage += "\n"
                    else:
                        resultMessage += queryResult
                    resultMessage += "```"
                    await ctx.send(resultMessage)       
                else:
                    await ctx.send("```Database has not been connected.```")
                    print("\nQuerying was cancelled because DB not connected.")
                return queryResult
            except Exception as e:
                eStr = f"Error: {e}\nQuery result: {queryResult}"
                print(eStr)
                await ctx.send(f"```{eStr}```")
                return None
        # If query string doesn't start with SELECT
        else:
            await ctx.send("```Querying is limited to SELECT only.```")
            print("\nQuerying was cancelled because statement didn't begin with SELECT.")
            print(f"Query string: {queryStr}")
    # If query string is empty
    else:
        await ctx.send("""```python
Query command usage:
%query "<sql_query_string>" (with quote)

Query string MUST begin with 'SELECT'
The table name is EVENTS.
The year in the DATE field of all records is 2010.
There are 4 fields in the EVENTS table:
- DATE
- TYPE ('BD' = 'Birthday', 'AN' = 'Anime Episode that has an Insert song', 'RE': 'Release of an important single or PV', 'SP': 'Special events')
- DETAILS: the detail of the event.
- NOTE: Note of the event. Abbreviated to optimize displaying on mobile phones.
- FULLNOTE: Note of the event. Not abbreviated.

Ex: %query "select * from events where date > '2010-4-1'"```""")

# Query events in a month
@bot.command()
async def events(ctx, month = datetime.now().month, full = None):
    monthName = datetime.now().strftime("%B")
    await ctx.send(f"List of events in {monthName}:")
    if (full == None):
        await botquery(ctx, f"\
            select date, type, details, note\
            from events where extract(month from date) = {month}", True)
    elif (full.lower() == "full"):
        await botquery(ctx, f"\
            select date, type, details, fullnote\
            from events where extract(month from date) = {month}", True)

# Query the next event
@bot.command()
async def nextev(ctx):
    print(f"\n'{ctx.message.content}' command called by {ctx.message.author}")
    currentDate = datetime.now().strftime("2010-%m-%d")
    events = query(f"select * from events where date = (select date from events where date > '{currentDate}' limit 1)")
    print(events)
    eventNo = 1
    eventTypes = {"BD": "Birthday", "AN": "Anime Episode with Insert Song", "RE": "Release", "SP": "Special"}

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

        embed.add_field(name = "Date",    value = (str(event[0].day) + "/" + str(event[0].month)), inline = False)
        embed.add_field(name = "Type",    value = eventTypes[event[1]]                           , inline = False)
        embed.add_field(name = "Details", value = event[2]                                       , inline = True)
        embed.add_field(name = "Note",    value = event[4]                                       , inline = True)
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
            elif re.match("đảng|đcs|cộng sản|3 que|3/|3///", message.content.lower()):
                await message.channel.send("<:dang:694251236895227965> "*3)
                triggered = True
            if (triggered): 
                print(f"\nMessage triggered: \"{message.content}\", Channel: #{message.channel.name}")

    except Exception as e:
        await message.channel.send(f"```Error: {e}```Honoka-chaaaaaan. Mite mite~")

    await bot.process_commands(message)

############# Run bot #############
bot.run(TOKEN)