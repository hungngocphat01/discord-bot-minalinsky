# Minalinsky Discord Bot

![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) 
![Discord](https://img.shields.io/badge/%3CServer%3E-%237289DA.svg?style=for-the-badge&logo=discord&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)

## Introduction
- This is a mini-bot that I wrote to serve as my administrative helper for my small Discord server of _Love Live Nijigasak'ic Forever VN_ (hence it's named _Minalinsky_, the legendary maid in the Love Live! universe).
- It only works in a very small scale (in a single server), so if you want to use this bot in your server (but I think you have no reason to do so), you will have to reconfigure the bot and re-setup the database.
- I'm also an moderator of a Vietnamese Love Live! fanpage, so the main purpose of this bot is to query upcoming events of the franchise and send a notification to the notification channel.
- This bot was originally written in Python when I was a first year student (with `discord.py`) and was the largest project (with over a thousand lines of Python code) I have ever made until it was deprecated. In August 2021, `discord.py` became deprecated, so I decided to migrate this bot to `discord.js`. A lot of legacy features (beginner developer's useless stuff) had been removed from the bot. I also reorganized the source code in the MVC model (maybe) for better maintainability.

## Features
- [x] Key feature: querying upcoming events of the Love Live! franchise (with PostgreSQL backend).
- [x] Automatically notify upcoming events in certain channels (hard-coded in the database).
- [x] Some basic commands like say, status, purge (delete messages)...
- [x] Auto react to certain messages containing certain emojis.
- [x] Response to hello, bye, g9, etc. (pre-programmed responses in the database).
- [ ] Approximate the value of a particular amount of love gem (SIF/SIFAS) in USD and VND.
- etc. (read the source code yourself).

## TODO
- [x] Implement authorization.
- [ ] Add images to notification.
- [ ] Prettify embeds.
- [ ] Confirmation (with buttons) when calling `purge`.
- [ ] Implement help command.
- [ ] Implement logging database and `journalctl`.

## Build & run
``` bash 
$ npm install
$ node deploy-commands.js
$ node Minalinsky.js
```
Under development.
