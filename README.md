# Minalinsky Discord Bot
Using Python, Discord.Cog and PostgreSQL.

## Introduction
- This is a simple bot written for my Discord guild ``Love Live µ'sic Forever VN``. Its main purpose is to query upcoming annual events of the Love Live! franchise (birthday, PV releases, etc. ) (since I'm a manager of a Vietnamese Love Live! fanpage).
- Written entirely from scratch (except libraries) during the COVID-19 lockdown in May 2020, when I wanted to ~~become a school idol~~ make my own Discord bot.
- Since I was still a freshman when I wrote this bot so there might be lots of mistakes in the source code. But, it's still functioning like a charm so I don't think I would need to replace those legacy codes.
- Ah yes, the the bot is named after the legendary Akihabara maid "Minalinsky" - or "Minami Kotori" in the Love Live! universe.
- I don't intend to expand this bot into a multi-server one, so there are lots of hard-coded IDs in the database. In other words, this bot is **NOT** ready to be fully functional on someone else's server except mine.

## Required libraries
- discord.py
- pytz
- pandas
- pandasql
- tabulate
- pygelbooru
- sqlalchemy
- psycopg2
- tqdm

## Features
- Key feature: querying upcoming events of the Love Live! franchise (with PostgreSQL backend).
- Automatically notify upcoming events in certain channels (hard-coded in the database).
- Some basic commands like `time`, `say`, ...
- Auto reaction to certain messages containing certain emojis.
- Fetch pics from ``gelbooru`` with/without the ``nsfw`` criteria.
- Response to ``hello``, ``bye``, ``g9``, etc. (pre-programmed responses in the database).
- Approximate the value of a particular amount of love gem (SIF) in USD and VND.
- Purge messages.
- etc. (read the source code yourself).

## Changelog
- Please read ``changelog.txt``.

## Environment variables
- ``RUNNING_ON_HEROKU`` (``0`` or ``1``): checks whether the bot is running on Heroku. This has to be set in your Heroku app settings. It will affect the bot's command prefix (e.g. one to trigger the Heroku instance and one to trigger the local instance).
- ``BOT_TOKEN``: bot token.
- `SEND_NEXT_EV`: whether to notify the next event at startup (to avoid spamming the notification channels while testing).
- `DATABASE_URL`: database connection string.
