# This file defines the basic events of the bot, including:
#   on_message
#   on_command_error
#   on_ready

# Discord modules
import discord
import json
from discord.ext import commands
import traceback
import re
import random
import os
from datetime import datetime
from BasicDefinitions import pquery
from Logging import *

class BotEventListeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.responses_json = json.load(open("responses.json"))
        log("Module loaded: BotEventListeners")
        
    ############# Bot events ############# 
    @commands.Cog.listener()
    async def on_ready(self):
        log("Bot ready.")

        # Query the next event
        for guild in self.bot.guilds:
            if int(os.getenv("DONT_SEND_NEXT_EV")):
                break
            if (guild.id == 694173494052651020):
                POLITBURO_CH = 694199808432537672
                NOTIF_CH = 694843380844331038
                
                channel = None

                currentDate = datetime.now().strftime("2010-%m-%d")
                events = pquery(f"select * from eventsdb where type = 'BD' and date = (select date from eventsdb where date > '{currentDate}' limit 1)").values.tolist()
                log("\nNext event(s) on startup:")
                log(events)
                eventNo = 1

                if (len(events) == 0):
                    break
                if (len(events) > 1):
                    await channel.send("Next events:")

                event_date_lst = str(events[0][0]).split()[0].split("-")
                event_date = datetime(int(event_date_lst[0]), int(event_date_lst[1]), int(event_date_lst[2]))
                curr_date = datetime(int(event_date_lst[0]), int(datetime.now().month), int(datetime.now().day))
                delta = (event_date - curr_date).days

                log("Date delta: ", delta)

                if (delta == 2):
                    channel = guild.get_channel(NOTIF_CH)
                elif (delta <= 4):
                    channel = guild.get_channel(POLITBURO_CH)
                else:
                    break

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
                        value = "Birthday",
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
                    await channel.send(embed = embed)
                    log("Event sent.\n")
                break
            break


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandNotFound):
            log(f"\nImproper '{ctx.message.content}' command called by {ctx.message.author}")
            await ctx.send(f"```Command not found: {ctx.message.content.split()[0]} ```")
        else:
            errorMsg = f"```Error: {error}\n"
            errorMsg += traceback.format_exc().replace('```', r'\```')
            errorMsg += "```"
            log(errorMsg)
            await ctx.send(errorMsg)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if "ponk" in message.content:
            if random.choices([0, 1], [0.7, 0.3])[0]:
                await message.add_reaction([e for e in message.guild.emojis if e.name == "ponk"][0])

        if "say" not in message.content:
            for regex in self.responses_json:
                if (re.search(regex, message.content.lower())):
                    randomRespond = random.choice(self.responses_json[regex])
                    await message.channel.send(randomRespond)
                    log(f"\nMessage triggered: \"{message.content}\", Channel: #{message.channel.name}")
                    log(f"Response: {randomRespond}")
                    break
