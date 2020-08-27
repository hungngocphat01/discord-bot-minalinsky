# This file is the main bot executable file. It does the following things
#   Init the bot
#   Import Cogs
#   Run the bot

# Discord modules
import discord
from discord.ext import commands
# Import basic definitions
from BasicDefinitions import COMMAND_PREFIX, TOKEN
# Import Cogs
from BasicCommands import BasicCommands
from BotEventListeners import BotEventListeners
from Emoji import Emoji
from EventQuery import EventQuery
from GelbooruSend import GelbooruSend
from SendHelpMsg import SendHelpMsg

bot = commands.Bot(command_prefix = COMMAND_PREFIX)
# Remove the discord's default help command
bot.remove_command("help")

############# Import Cogs #############
bot.add_cog(BotEventListeners(bot))
bot.add_cog(BasicCommands(bot))
bot.add_cog(EventQuery(bot))
bot.add_cog(Emoji(bot))
bot.add_cog(GelbooruSend(bot))
bot.add_cog(SendHelpMsg(bot))

############# Run bot #############
try:
    bot.run(TOKEN)
except Exception as e:
    print(f"Bot stopped working due to error: \n{e}")