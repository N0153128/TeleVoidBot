# coding=utf8
from newbot import Bot
from tools import logmod
from mods import mods
import time
from mods import teleworker
import asyncio
from multiprocessing import Process
import sys

# initializing objects
bot = Bot(token=sys.argv[1])
print(f'\nUsing token: {bot.token}\n')
mods = mods.Mods()
log = logmod.Loger()
# spam = spam.Spam()

# initializing variables
upd = bot.link + '/getUpdates'
queue = asyncio.Queue()
localtime = time.asctime(time.localtime(time.time()))

# printing startup message
print(f'Started @ {localtime}')
print('Activated...')


# defining the function that would look up for updates and put it in a queue. every message that bot receives gets
# logged. when this function receives a message - it checks for spamming. if spam returns true - it will start up a
# process that would handle the message.
async def putin(q):
    while True:
        try:
            data = await bot.get_all()
            offset = bot.get_id(data) + 1
            await log.log_saver(str(bot.get_name(data)), str(bot.get_from_id(data)), str(bot.get_message(data)),
                                bot.get_chat_type(data), bot.get_chat_id(data), bot.get_username_or_first_name(data))
            # if spam.checker(bot.get_chat_id(data)):
            await q.put(data)
            await bot.session.get(bot.link + '/getUpdates?offset=' + str(offset))
            await putout(queue)
            # elif not spam.checker(bot.get_chat_id(data)):
            #     requests.get(bot.link + '/getUpdates?offset=' + str(offset))
        except (IndexError, KeyError, TypeError):
            pass


async def gen(data):
    d = await data.get()
    yield d


# this function is the message handler. every command is hardcoded for both private and group chats
async def putout(q):
    async for item in gen(q):
        try:
            # callbacks
            if bot.is_callback(item):
                pass

            # messages
            # Telegraph
            elif bot.get_message(item).startswith('/save'):
                await mods.note_handler(item)
            elif bot.get_message(item) == '/showmine':
                await mods.send_keys(item)
            elif bot.get_message(item) == '/clear':
                await mods.clear(item)
            elif bot.get_message(item) == 'inline':
                await bot.send_message(item, 'Here is your inline: ', inline=['suka', 'pidor', 'gandon'],
                                       callback=True)
        except Exception as e:
            print(e)

loop = asyncio.get_event_loop()
loop.run_until_complete(putin(queue))

# starting processes that would check for new messages and start adding currency for the consignments
