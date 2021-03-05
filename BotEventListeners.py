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
from Logging import *
from EventQuery import event_notifier

class BotEventListeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("configuration.json", mode="rt") as f:
            conf = json.loads(f.read())
            self.responses_json = conf["responses"]
            self.emoji_replies = conf["emoji_replies"]

        log("Module loaded: BotEventListeners")
        
    ############# Bot events ############# 
    @commands.Cog.listener()
    async def on_ready(self):
        log("Bot ready.")

        game = discord.Game("with Honoka-chan")
        await self.bot.change_presence(status=discord.Status.idle, activity=game)

        # Query the next event
        await event_notifier(self.bot)

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
        for e in self.emoji_replies:
            if e in message.content and random.choices([0, 1], [0.7, 0.3])[0]:
                await message.add_reaction([x for x in message.guild.emojis if x.name == e][0])

        if "say" not in message.content and not message.author.bot:
            for regex in self.responses_json:
                if (re.search(regex, message.content.lower())):
                    randomRespond = random.choice(self.responses_json[regex])
                    await message.channel.send(randomRespond)
                    log(f"\nMessage triggered: \"{message.content}\", Channel: #{message.channel.name}")
                    log(f"Response: {randomRespond}")
                    break
