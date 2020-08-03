# Discord modules
import discord
from discord.ext import commands
from datetime import datetime
from BasicDefinitions import pquery, eventsdb, query, COMMAND_PREFIX

class EventQuery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Module loaded: EventQuery")

    # Query command
    @commands.command(aliases = ["query"])
    async def botquery(self, ctx, queryStr = None):
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
    @commands.command()
    async def events(self, ctx, month = None, full = None):
        try:
            if (str(month).lower() == "full"):
                month = datetime.now().month
                full = "full"
            elif (month == None):
                month = datetime.now().month

            monthName = datetime(2020, int(month), 1).strftime("%B")

            await ctx.send(f"List of events in {monthName}:")
            if (full == None):
                await self.botquery(ctx, f"select strftime('%d', date) as day, type, details, note from eventsdb where cast(strftime('%m', date) as integer) = {month}")
            elif (full.lower() == "full"):
                await self.botquery(ctx, f"select strftime('%d', date) as day, type, details, fullnote from eventsdb where cast(strftime('%m', date) as integer) = {month}")
        except Exception as e:
            await ctx.send(f"``Error: {e}``")
            print(f"\nError: {e}")

    # Query the next event
    @commands.command()
    async def nextev(self, ctx):
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