# coding=utf8
from telegram_handler import Bot
from tools import logmod
from mods import mods
import time
from mods import teleworker
import asyncio
from settings import *


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


class Initial():
    def __init__(self):
        self.bot = Bot(BOT_KEY)
        self.send = self.bot.send_message
        self.get = self.bot.get_message
        self.queue = asyncio.Queue()
        self.upd = self.bot.link + '/getUpdates'
        self.log = logmod.Loger()
        self.teleworker = teleworker.Worker()
        self.localtime = time.asctime(time.localtime(time.time()))
        self.launchtime = time.time()

    async def feed(self, data):
        d = await data.get()
        yield d

    def startup_time(self):
        print(f'Started @ {self.localtime}')
        print('Activated...')
