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
from datetime import datetime
from BasicDefinitions import pquery

class BotEventListeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.responses_json = json.load(open("responses.json"))
        print("Module loaded: BotEventListeners")
        
    ############# Bot events ############# 
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot ready.")

        # Query the next event
        for guild in self.bot.guilds:
            if (guild.id == 694173494052651020):
                for channel in guild.channels:
                    if (channel.id == 694843380844331038):
                        currentDate = datetime.now().strftime("2010-%m-%d")
                        events = pquery(f"select * from eventsdb where type = 'BD' and date = (select date from eventsdb where date > '{currentDate}' limit 1)").values.tolist()
                        print("\nNext event(s) on startup:")
                        print(events)
                        eventNo = 1

                        if (len(events) == 0):
                            break
                        if (len(events) > 1):
                            await channel.send("Next events:")

                        event_date_lst = str(events[0][0]).split()[0].split("-")
                        event_date = datetime(int(event_date_lst[0]), int(event_date_lst[1]), int(event_date_lst[2]))
                        curr_date = datetime(int(event_date_lst[0]), int(datetime.now().month), int(datetime.now().day))
                        delta = (event_date - curr_date).days

                        print("Date delta: ", delta)

                        if (delta != 2):
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
                            print("Event sent.\n")
                        break
            break


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandNotFound):
            print(f"\nImproper '{ctx.message.content}' command called by {ctx.message.author}")
            await ctx.send(f"```Command not found: {ctx.message.content.split()[0]} ```")
        else:
            errorMsg = f"```Error: {error}\n"
            errorMsg += traceback.format_exc().replace('```', r'\```')
            errorMsg += "```"
            print(errorMsg)
            await ctx.send(errorMsg)

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if "say" not in message.content:
                for regex in self.responses_json:
                    if (re.search(regex, message.content.lower())):
                        randomRespond = random.choice(self.responses_json[regex])
                        await message.channel.send(randomRespond)
                        print(f"\nMessage triggered: \"{message.content}\", Channel: #{message.channel.name}")
                        print(f"Response: {randomRespond}")
                        break
        except Exception as e:
            await message.channel.send(f"```Error: {e}```Honoka-chaaaaaan. Mite mite~")