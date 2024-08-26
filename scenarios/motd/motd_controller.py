# coding=utf8
from telegram_handler import Bot
import time
import asyncio
import sys
from scenarios.motd.motd import *
from config import *
from settings import *

motd = Motd(API_KEY)
bot = Bot(BOT_KEY)
send = bot.send_message
get = bot.get_message
# print(f'\nUsing token: {bot.token}\n')

# initializing variables
upd = bot.link + '/getUpdates'
queue = asyncio.Queue()
localtime = time.asctime(time.localtime(time.time()))
launchtime = time.time()

# printing startup message
# print(f'Started @ {localtime}')
# print('Activated...')

motd_commands = ['/start']

async def feed(data):
    d = await data.get()
    yield d

# this function is the message handler. every command is hardcoded for both private and group chats
async def motd_handler(q,):
    try:
        if get(q) == '/start':
            await send(q, message=await motd.begin_push(q))

    except Exception as e:
        print(e)

# async def motd_loop():
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(bot.loop_void(queue=queue, data_resolver=webapi_handler))

# starting processes that would check for new messages and start adding currency for the consignments