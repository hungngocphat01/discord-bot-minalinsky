# Minalinsky Discord Bot
Using Python and Discord.Cog.

## Introduction
- This is a simple bot written for my Discord guild ``Love Live µ'sic Forever VN``. Its main purpose is querying upcoming annual events of the Love Live! franchise (birthday, PV releases, etc. ) (since I'm a manager of a Vietnamese Love Live! fanpage).
- Written entirely from scratch (except libraries) during the COVID-19 lockdown in May 2020, when I wanted to ~~become a school idol~~ make my own Discord bot.
- As I was still a freshman when I made this so there might be lots of mistakes in my code. But yep, it's still running fine to date so I won't fix it except when it breaks down someday (or simply I had realized my mistakes). :P
- Ah yes, the the bot is named after the legendary Akihabara maid "Minalinsky" - or "Minami Kotori" (in the Love Live! universe of course).
- I don't intend to expand this bot into a multiserver one, so there are lots of hard-coded IDs in the source code. It means that this bot is NOT ready to work on any other server but the aforementioned one. You have to edit the variables yourself in order for it to work as expected.

## Required libraries
- discord.py
- pytz
- sqlite3
- tabulate
- xlrd
- pygelbooru

## Features
- Key feature: querying upcoming events of the Love Live! franchise (using SQLite).
- Automatically notify 1 day prior to next event (exclusive to only one server and hard-coded).
- Some basic commands like `time`, `say`, ...
- Auto reaction to certain messages containing certain emojis.
- Send custom emojis (defined in the ``emoji.json`` file). This is pretty useless tho. Use NQN instead.
- Fetch pics from ``gelbooru`` with/without the ``nsfw`` criteria.
- Response to ``hello``, ``bye``, ``g9``, etc. (pre-programmed responses in the configuration file).
- Calculate the value of a particular amount of love gem in USD and VND.
- Purge messages.
- etc. (read the source code yourself).

## Changelog
- Please refer to ``changelog.txt``.

## Environment variables
- ``RUNNING_ON_HEROKU`` (``0`` or ``1``): checks whether the bot is running on Heroku. This has to be set in your Heroku app settings. It will affect the bot's command prefix (e.g. one to trigger the Heroku instance and one to trigger the local instance).
- ``BOT_TOKEN``: bot token.
- DONT_SEND_NEXT_EV: do not notify the next event at startup (to avoid spamming in notification channels while testing).
