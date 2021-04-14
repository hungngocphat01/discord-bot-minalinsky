# Discord modules
import discord
import tabulate
import pytz
import sqlite3
import os
import re
from discord.ext import commands
from datetime import date, datetime
from Administration import is_admin
from BasicDefinitions import COMMAND_PREFIX
from Logging import *

try:
    db_conn = sqlite3.connect("events.db")
except:
    db_conn = None

def query_execute(sql: str):
    if (db_conn == None):
        log("Database not connected.")
        return None
    
    result_lst = []

    result_tbl = db_conn.execute(sql)
    col_names = [description[0] for description in result_tbl.description]

    for row_data in result_tbl:
        row_dict = {}
        for i in range(len(col_names)):
            if row_data[i] != "":
                row_dict[col_names[i]] = row_data[i]
            else:
                row_dict[col_names[i]] = "--"
        result_lst.append(row_dict)

    return result_lst

def make_discord_embeds(events: list) -> list:
    result = []

    for event in events:
        embed = discord.Embed()
        embed.title = "Next event"
        embed.add_field(name="Date", value="{0}/{1}".format(event["day"], event["month"]))
        embed.add_field(name="Type", value=event["type"])
        embed.add_field(name="Details", value=event["details"])
        embed.add_field(name="Note", value=event["note"])
        embed.color = discord.Color.orange()

        result.append(embed)
    
    return result

def get_next_events() -> list:
    hcm_time = pytz.timezone("Asia/Ho_Chi_Minh")
    now = datetime.now(hcm_time)

    sql = """select * from events
        where month = {0} and
        day == (
            select min(day)
            from events
            where day >= cast(strftime('%d', 'now') as int) and month == {0}
        )""".format(now.month)
    query_result = query_execute(sql)

    return query_result

class EventQuery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        log("Module loaded: EventQuery")

    
    @commands.command()
    async def query(self, ctx, *, sql=None):
        command_log(ctx)
        if (sql == None):
            helpmsg = f"""
**Syntax:** `{COMMAND_PREFIX}query <sql statement>`
This command will execute an SQLite statement in the events database. This database has only one table, named 'events' as well.
Line breaks are supported.
Do not perform any SQL injection because you simply can't.

**Table schema:**
```sql
CREATE TABLE events (
    day         int,
    month       int,
    type        nvarchar(5),
    details     nvarchar(50),
    short_note  nvarchar(50),
    note        nvarchar(50)
);```
**Example 1:** Query events in a month
```sql
{COMMAND_PREFIX}query select day, month, details from events where month=4 and type="BD"```
**Example 2:** Query the nearest next event(s)
```sql
{COMMAND_PREFIX}query select * from events
where month = cast(strftime('%m', 'now') as int) and
day == (
    select min(day)
    from events
    where day >= cast(strftime('%d', 'now') as int) and month == cast(strftime('%m', 'now') as int)
);```"""
            await ctx.send(helpmsg)
            return

        if (db_conn == None):
            await ctx.send("```Database not connected.```")
            return

        if re.match("alter|insert|delete|update|drop|create", sql.lower()):
            log("SQL injection detected.")
            await ctx.send("```Trying to perform an SQL injection attack huh?```")
            return
    
        query_result = query_execute(sql)
        fmt_table = tabulate.tabulate(query_result, headers="keys")

        await ctx.send(f"```glsl\nQuery result:\n\n{fmt_table}```")

    @commands.command()
    async def events(self, ctx, month=None, full=None):
        if (db_conn == None):
            ctx.send("```Database not connected.```")
            return

        if month is None:
            hcm_time = pytz.timezone("Asia/Ho_Chi_Minh")
            now = datetime.now(hcm_time)
            month = now.month
        
        if full is None:
            note = "short_note"
        else:
            note = "note"
        
        sql = "select day, type, details, {0} from events where month = {1} order by day asc".format(note, month)

        query_result = query_execute(sql)
        fmt_table = tabulate.tabulate(query_result, headers="keys")

        await ctx.send(f"```glsl\nQuery result:\n\n{fmt_table}```")
    
    @commands.command()
    async def nextev(self, ctx):
        if (db_conn == None):
            await ctx.send("```Database not connected.```")
            return
        
        next_events = get_next_events()
        if (len(next_events) == 0):
            await ctx.send("```No next event.```")
            return 
        for embed in make_discord_embeds(next_events):
            await ctx.send(embed=embed)

# For use in my guild only (the creator's guild)
async def event_notifier(bot):
    if os.getenv("SEND_NEXT_EV") == "0":
        log("Not sending next event.")
        return

    POLITCH = 694199808432537672
    NOTIFCH = 694843380844331038

    events = get_next_events()

    for event in events:
        print(event)

    if (len(events) == 0):
        log("No next event to display.")
        return
    
    hcm_time = pytz.timezone("Asia/Ho_Chi_Minh")
    now = datetime.now(hcm_time)

    event_day = events[0]["day"]

    delta_day = event_day - now.day
    print("Delta day:", delta_day)

    if delta_day in (0, 1):
        destination_channel = bot.get_channel(NOTIFCH)
    elif delta_day in (2, 3):
        destination_channel = bot.get_channel(POLITCH)
    else:
        return
    
    for embed in make_discord_embeds(events):
        await destination_channel.send(embed=embed)
    


    