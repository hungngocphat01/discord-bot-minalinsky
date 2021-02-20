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
import pandas as pd
import pandasql
from tabulate import tabulate
from Logging import *

# Bot info
ver = "3.9.2"
date = "20/02/2021"
runningOnHeroku = (os.getenv("RUNNING_ON_HEROKU") == "1")

log(f"Minalinsky Discord Bot v{ver}")
log(f"Last updated {date}")
log(f"Scripted in Python 3.")
log(f"(c) 2020-2021 Hung Ngoc Phat")
log("================================")

#############  Read the database #############
# Import database
eventsdb = None

try:
    eventsdb = pd.read_excel("events.xls")
except FileNotFoundError:
    log("Database file not found. Please check again.")

# Init pandasql
pquery = lambda queryStr: pandasql.sqldf(queryStr, globals())
query = lambda queryStr: tabulate(pquery(queryStr), showindex = False, headers = [])

#############  Supporting functions #############

def getTime(zone):
    now_utc = datetime.now(pytz.timezone("UTC"))
    now_zone = now_utc.astimezone(pytz.timezone(zone))
    return now_zone.strftime("%d/%m/%Y, %H:%M:%S")

def similarityBetween(str1, str2):
    same = 0
    n1 = len(str1)
    n2 = len(str2)

    if n1 > n2:
        Range = range(0, n2)
    else:
        Range = range(0, n1)
    for i in Range:
        if str1[i] == str2[i]:
            same += 1
    return same

#############  Init bot ############# 
TOKEN = str(os.getenv("BOT_TOKEN"))
COMMAND_PREFIX = "%"

startTime = datetime.now()
startTimeStr = getTime("Asia/Ho_Chi_Minh")

if runningOnHeroku:
    COMMAND_PREFIX = "%"
else:
    COMMAND_PREFIX = "&"
