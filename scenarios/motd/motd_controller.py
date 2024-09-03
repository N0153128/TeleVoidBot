# coding=utf8
# from scenarios.motd.boilerplate import *
from initial import Initial
from scenarios.motd.motd import Motd
from config import *

base = Initial()
motd = Motd(API_KEY)

motd_commands = ['/start']

async def motd_handler(q,):
    try:
        if base.get(q) == '/start':
            await base.send(q, message=await motd.begin_push(q))

    except Exception as e:
        print(e)
