# This file defines the basic events of the bot, including:
#   on_message
#   on_command_error
#   on_ready

# Discord modules
import discord
from discord.ext import commands
import traceback
import re
import random
from datetime import datetime
from BasicDefinitions import pquery

class BotEventListeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
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
                            await channel.send("The previous event is the final one within this year. See you again next year :penguin: ")
                            break
                        if (len(events) > 1):
                            await channel.send("Next events:")

                        event_date_lst = str(events[0][0]).split()[0].split("-")
                        event_date = datetime(int(event_date_lst[0]), int(event_date_lst[1]), int(event_date_lst[2]))
                        curr_date = datetime(int(event_date_lst[0]), int(datetime.now().month), int(datetime.now().day))
                        delta = (event_date - curr_date).days

                        print("Date delta: ", delta)

                        if (delta != 1):
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
        triggered = False
        try:
            if "say" not in message.content:
                # Mentioned
                if "694191159949393980" in message.content.lower():
                    responds = [
                        f"J kêu cc",
                        "J kêu gì",
                        "J có gì ko",
                        "J"
                        ]
                    await message.channel.send(random.choice(responds))
                    triggered = True
                # Hello
                if "hello" in message.content.lower():
                    responds = [
                        f"Okaerinasai, {message.author.name}-sama!",
                        "Lô lô cc",
                        "Hai~. Okaeri~",
                        "Konnichiwa~"
                        ]
                    await message.channel.send(random.choice(responds))
                    triggered = True
                # Good night
                elif (re.search("g9|good night|oyasumi|đi ngủ", message.content.lower())) and (message.author.id != self.bot.user.id):
                    responds = [
                        "Oyasuminasaiiiii~",
                        "J ngủ ngon",
                        "J chúc gặp nhiều ác mộng nha",
                        "J giờ này mà ngủ à. Sớm thế"
                        ]
                    await message.channel.send(random.choice(responds))
                    triggered = True
                # Bye
                elif "bye" in message.content.lower():
                    responds = [
                        "Mata ne~~",
                        "Jaa ne~",
                        "Byeee~",
                        "J đi luôn đi"
                        ]
                    await message.channel.send(random.choice(responds))
                    triggered = True
                # DCSVN
                elif re.match("đảng|đcs|cộng sản|vn|việt nam|vietnam", message.content.lower()):
                    await message.channel.send("<:dang:694251236895227965> "*3)
                    triggered = True
                if (triggered): 
                    print(f"\nMessage triggered: \"{message.content}\", Channel: #{message.channel.name}")

        except Exception as e:
            await message.channel.send(f"```Error: {e}```Honoka-chaaaaaan. Mite mite~")