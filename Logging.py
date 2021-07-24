from os import replace
from datetime import datetime
from BasicDefinitions import Base, session
from dateutil.parser import isoparse

def log(*args):
    objs = list(args)
    for i in range(0, len(objs)):
        if isinstance(objs[i], str):
            objs[i] = str(objs[i]).replace("`", "@")
    objs = [str(x) for x in objs]
    msg = " ".join(objs)

    now = datetime.now()
    try:
        SystemLog = Base.classes.systemlog
        log_entry = SystemLog(time=now, content=msg)
        session.add(log_entry)
        session.commit()
    except:
        session.rollback()
        raise
    
    print("[%s] " % datetime.strftime(now, "%Y-%m-%d %H:%M") + msg)


def command_log(ctx):
    log(f"In channel {ctx.message.channel}, {str(ctx.message.author)} invoked command: {ctx.message.content}")
