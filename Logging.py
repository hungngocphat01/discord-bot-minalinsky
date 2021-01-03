from os import replace


runtime_logs = []

def log(obj):
    if isinstance(obj, str):
        obj = str(obj).replace("```", "@@@")
    print(obj)
    runtime_logs.append(obj)

def command_log(ctx):
    log(f"In channel {ctx.message.channel}, {str(ctx.message.author)} invoked command: {ctx.message.content}")
