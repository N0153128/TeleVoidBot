# coding=utf8
from telegram_handler import Bot
from tools import logmod
from mods import mods
import time
from mods import teleworker
import asyncio
from multiprocessing import Process
import sys
from web import RestfulInteract
from settings import ADMIN


bot = Bot(token=sys.argv[1])
send = bot.send_message
get = bot.get_message
print(f'\nUsing token: {bot.token}\n')
mods = mods.Mods()
log = logmod.Loger()
teleworker = teleworker.Worker()
rest = RestfulInteract()

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
            if admin:
                if bot.get_chat_id(item) == ADMIN:
                    await command_cycle(item)
            elif not admin:
                  await command_cycle(item)

        except Exception as e:
            print(e)

async def command_cycle(data):
    if get(data) == '/debug':
        await send(data, 'Ping')
    elif get(data).startswith('/post'):
        title, text = rest.get_data(bot.get_message(data))
        rest.post(title, text)
        await send(data, 'Post sent!')


loop = asyncio.get_event_loop()
loop.run_until_complete(bot.loop_void(queue=queue, data_resolver=webapi_handler))

# starting processes that would check for new messages and start adding currency for the consignments


mock = '''
24 have passed, wake up.
Current Weather:
# Highest temperature today: 
# Rain possibility:

Ton wallet balance: +
Ton wallet value: +

Repo 1: number of commits +
Repo 2: number of commits +
Repo 3: number of commits +
Repo 4: number of commits +

Unread emails: 

Ton difference: (24h)


'''