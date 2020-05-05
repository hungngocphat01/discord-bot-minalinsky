# This file defines the basic events of the bot, including:
#   on_message
#   on_command_error
#   on_ready

# Discord modules
import discord
from discord.ext import commands
import traceback
import re

class BotEventListeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    ############# Bot events ############# 
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot ready.")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandNotFound):
            print(f"\nUnexisted '{ctx.message.content}' command called by {ctx.message.author}")
            await ctx.send(f"```Command not found: {ctx.message.content.split()[0]} ```")
        else:
            errorMsg = f"```Error: {error}\n"
            errorMsg += traceback.format_exc().replace('```', r'\```')
            errorMsg += "```"
            print(errorMsg)
            await ctx.send(errorMsg)
        raise error

    @commands.Cog.listener()
    async def on_message(self, message):
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
                elif (re.search("g9|night|good|oyasumi|ngủ", message.content.lower())) and (message.author.id != self.bot.user.id):
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