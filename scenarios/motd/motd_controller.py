# coding=utf8
# from scenarios.motd.boilerplate import *


motd_commands = ['/start']

async def motd_handler(q,):
    try:
        if get(q) == '/start':
            await send(q, message=await motd.begin_push(q))

    except Exception as e:
        print(e)
