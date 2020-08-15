# Minalinsky Discord Bot
Using Python and Discord.Cog.

## Introduction
- This is a simple bot written for my Discord guild ``Love Live µ'sic Forever VN``. Its main purpose is querying upcoming annual events of the Love Live! franchise (birthday, PV releases, etc. ) (since I'm a manager of a Vietnamese Love Live! fanpage).
- Written entirely from scratch (except libraries) during COVID-19 lockdown in May 2020, when I wanted to ~~become a school idol~~ make my own Discord bot.
- As I was still a freshman when I made this so there might be mistakes (and lots of C-like programming style) in my code. But yep, it's still running fine so I won't fix it except when it breaks down someday (or simply I had realized my mistakes). :P
- Ah yes, the the bot is named after the legendary Akihabara maid "Minalinsky" - or "Minami Kotori" (in the Love Live! universe of course).

## Required libraries
- discord.py
- pytz
- pandas
- pandasql
- tabulate
- xlrd
- pygelbooru

## Features
- Key feature: querying upcoming events of the Love Live! franchise (using pandasql to simulate SQLite's behavior).
- ``say`` command.
- ``time`` command.
- Send custom emojis (defined in the ``emoji.json`` file).
- Fetch pics from ``gelbooru`` with ``nsfw`` toggle.
- Response to ``hello``, ``bye``, ``g9``, etc. (in Vietnamese and Japanese).
- Calculate the value of a particular amount of love gem in USD and VND.
- Purge messages.
- Etc.

## Environment variables
- ``RUNNING_ON_HEROKU`` (``0`` or ``1``): checks whether the bot is running on Heroku. This has to be set in your Heroku app settings. It will affect the bot's command prefix (e.g. one to trigger the Heroku instance and one to trigger the local instance).
- ``BOT_TOKEN``: bot token.
