# coding=utf8
from telegram_handler import Bot
from tools import logmod
from mods import mods
import time
from mods import teleworker
import asyncio
# from web import RestfulInteract
from settings import *
# from scenarios.motd.motd_controller import motd_loop
from scenarios.motd.motd_controller import motd_handler, motd_commands

# NOTE FOR EVERYONE WHO'S WILLING TO UNDERSTAND THE CODE INSIDE OTHER FILES
# Key-Arguments: data, fore, inline, get_chat, item, dirty
# data: data usually represents a product of get_all method, which returns json object with necessary data that is
# needed for all requests and messages. sometimes this argument can only pass 'raw' or 'clean' data, which is plain
# string, integer, float, bool.
# dirty: arbitrary argument used to 'clean' the information that is needed from 'data' argument. 'dirty' data
# represents dicts and lists.
# item: same as data, but almost never represents clean data
# fore: arbitrary argument, represents a switch. if specified - method will return different set of data
# inline: arbitrary argumet, represents switch for inline keyboard mode, which adds fancy buttons for the message
# get_chat: arbitrary argument, if specified - uses get_chat_id, instead of get_from_id

# initializing objects
bot = Bot(BOT_KEY)
send = bot.send_message
get = bot.get_message
print(f'\nUsing token: {bot.token}\n')
log = logmod.Loger()
teleworker = teleworker.Worker()
# rest = RestfulInteract()
# motd = motd.Motd(api_key='AE55VET32XKPKIAAAAAMVUYLXFDRRK2RAWDDJJEHZ4TQAJ27BVPNTAMSRCJ7TMQDXQPZ3DY')

# initializing variables
# upd = bot.link + '/getUpdates'
# queue = asyncio.Queue()
# localtime = time.asctime(time.localtime(time.time()))
# launchtime = time.time()

# printing startup message
# print(f'Started @ {localtime}')
# print('Activated...')


# async def feed(data):
#     d = await data.get()
#     yield d

class initial:
    def __init__(self, bot):
        self.bot = bot(BOT_KEY)
        self.send = bot.send_message
        self.get = bot.get_message
        self.queue = asyncio.Queue()
        self.upd = bot.link + '/getUpdates'
        self.motd = motd.Motd(API_KEY)

    async def feed(self, data):
        d = await data.get()
        yield d

    async def startup_time(self):
        print(f'Started @ {self.localtime}')
        print('Activated...')
