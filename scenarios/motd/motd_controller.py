# coding=utf8
from telegram_handler import Bot
import time
import asyncio
import sys
from settings import ADMIN
from scenarios.motd.motd import *
from config import *
from settings import *

motd = Motd(API_KEY)
bot = Bot(BOT_KEY)
send = bot.send_message
get = bot.get_message
print(f'\nUsing token: {bot.token}\n')

# initializing variables
upd = bot.link + '/getUpdates'
queue = asyncio.Queue()
localtime = time.asctime(time.localtime(time.time()))
launchtime = time.time()

# printing startup message
print(f'Started @ {localtime}')
print('Activated...')


async def feed(data):
    d = await data.get()
    yield d

# this function is the message handler. every command is hardcoded for both private and group chats
async def webapi_handler(q, admin):
    async for item in feed(q):
        try:
            # callbacks
            if bot.is_callback(item):
                pass

            # messages
            if get(item) == '/start':
                if admin:
                    if bot.get_chat_id(item) == ADMIN:
                        await send(item, message=await motd.begin_push(item))
                elif not admin:
                    pass

        except Exception as e:
            print(e)

async def motd_loop():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.loop_void(queue=queue, data_resolver=webapi_handler))

# starting processes that would check for new messages and start adding currency for the consignments