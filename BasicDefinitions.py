# This file is the basic definition file. It defines the following things:
#   Bot info
#   Database source file
#   Emoji json
#   Supporting functions

# Discord modules
import discord
from discord.ext import commands
# Supporting modules
from datetime import datetime
import re
import json
import pytz
import os
# Database simulation libraries
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from Logging import *

# Bot info
ver = "5.0.1 beta"
date = "22/07/2021"
runningOnHeroku = (os.getenv("RUNNING_ON_HEROKU") == "1")

log(f"Minalinsky Discord Bot v{ver}")
log(f"Last updated {date}")
log(f"Scripted in Python 3.")
log(f"(c) 2020-2021 Hung Ngoc Phat")
log("================================")

#############  Supporting functions #############

def getTime(zone):
    now_utc = datetime.now(pytz.timezone("UTC"))
    now_zone = now_utc.astimezone(pytz.timezone(zone))
    return now_zone.strftime("%d/%m/%Y, %H:%M:%S")

#############  Load database  #############
db_url = os.getenv("DATABASE_URL")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://")
Base = automap_base()
engine = create_engine(db_url)

# Reflect the tables
Base.prepare(engine, reflect=True)

# Start new session
session = Session(engine)
session_state = lambda: session.is_active
#############  Init bot ############# 
TOKEN = str(os.getenv("BOT_TOKEN"))
COMMAND_PREFIX = "%"

startTime = datetime.now()
startTimeStr = getTime("Asia/Ho_Chi_Minh")

if runningOnHeroku:
    COMMAND_PREFIX = "%"
else:
    COMMAND_PREFIX = "&"
