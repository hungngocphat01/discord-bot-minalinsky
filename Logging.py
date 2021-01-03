from os import replace


runtime_logs = []

def log(*args):
    objs = list(args)
    for i in range(0, len(objs)):
        if isinstance(objs[i], str):
            objs[i] = str(objs[i]).replace("```", "@@@")
    msg = " ".join(str(objs))
    print(msg)
    runtime_logs.append(msg)

def command_log(ctx):
    log(f"In channel {ctx.message.channel}, {str(ctx.message.author)} invoked command: {ctx.message.content}")
