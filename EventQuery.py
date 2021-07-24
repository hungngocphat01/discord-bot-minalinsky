# Discord modules
from os import pardir
import discord
import tabulate
from discord.ext import commands
from datetime import date, datetime
from DatabaseManagement import is_admin, query_settings, mark_as_notified, legacy_query_execute, tabular_format
from BasicDefinitions import COMMAND_PREFIX, runningOnHeroku, session
import pandas as pd
from tabulate import tabulate
from Logging import *
import os

#select * from events where month=7 and day = (select min(day) from events where month = 7 and day >= extract(day from now()));

class EventQuery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        log("Module loaded: EventQuery")

    @commands.command()
    async def query(self, ctx, sql=None):
        command_log(ctx)
        if (sql == None):
            await ctx.send("```Please refer to the help command.```")
            return 

        # Check for the first word
        print(sql.split()[0].lower())
        if sql.split()[0].lower() != "select":
            await ctx.send("```Only select statements are allowed.```")
            return 
        
        try:
            result_lst = legacy_query_execute(sql)
            fmt_table = tabular_format(result_lst)
            await ctx.send(f"```glsl\nQuery result:\n\n{fmt_table}```")
        except:
            raise

    @staticmethod        
    def get_next_events(ignore_notified: bool = False):
        this_year = datetime.now().year
        notification_filter = ""
        if ignore_notified:
            notification_filter = "and notified='false'"

        sql = f"""select * 
from events 
where make_date({this_year}, month, day) = (
    select min(make_date({this_year}, month, day)) 
    from events 
    where make_date({this_year}, month, day) >= now()::date {notification_filter}
);"""   
        return legacy_query_execute(sql)

    @staticmethod
    def make_vietnamese_notification(events: list):
        parts = []
        parts.append("**Sự kiện sắp tới:**")

        for event in events:
            s: str
            if event["type"] == "BD":
                desc = " (%s)" % event["note"] if len(event["note"]) > 0 else ""
                s = "- Sinh nhật của %s%s" % (event["details"], desc)
            elif event["type"] == "PV":
                s = "- PV '%s' (%s) đã được ra mắt" % (event["details"], event["note"])
            elif event["type"] == "AN":
                s = "- Tập anime '%s' đã được chiếu, có insert song: '%s'" % (event["details"], event["note"])
            elif event["type"] == "RE":
                s = "- Đĩa đơn '%s' (%s) đã được ra mắt" % (event["details"], event["note"])
            elif event["type"] == "SP":
                s - "- Sự kiện đặc biệt: %s" % event["details"] 
            s += " vào ngày %d/%d." % (event["day"], event["month"])
            parts.append(s)
            
        return "\n".join(parts)
    
    @commands.command()
    async def nextev(self, ctx, month=None):
        command_log(ctx)
        if (month == None):
            month = datetime.now().month
        
        message = self.make_vietnamese_notification(self.get_next_events())
        await ctx.send(f"{message}")
    
    @staticmethod
    async def event_notifier(bot):
        if os.getenv("SEND_NEXT_EV") == "0":
            log("Not sending next event.")
            #return
        
        events = EventQuery.get_next_events(ignore_notified=True)
        if len(events) == 0:
            log("No next event to display.")
            return            
        log(events[0]["day"], events[0]["month"], events[0]["type"], events[0]["details"])
        event_day = int(events[0]["day"])
        event_month = int(events[0]["month"])
        event_date = datetime(datetime.now().year, event_month, event_day)
        date_diff = event_date - datetime.now()

        log("Date difference until next:", date_diff)

        if date_diff.days in [2, 3]:
            notify_channel_id = query_settings("pre-notify-channel-id")
        elif date_diff.days in [0, 1]:
            notify_channel_id = query_settings("notify-channel-id")
            mark_as_notified(event_day, event_month)
        else:
            log("Next event does not lie within notify range.")
            return
        
        destination_channel: discord.TextChannel = bot.get_channel(notify_channel_id)
        await destination_channel.send(content=EventQuery.make_vietnamese_notification(events))
        log(f"Message sent to {str(destination_channel)}")