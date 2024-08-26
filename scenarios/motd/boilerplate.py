# coding=utf8
from telegram_handler import Bot
import time
import asyncio
from scenarios.motd.motd import *
from config import *
from settings import *

# motd = Motd(API_KEY)
# bot = Bot(BOT_KEY)
# send = bot.send_message
# get = bot.get_message

# upd = bot.link + '/getUpdates'
# queue = asyncio.Queue()

# async def feed(data):
#     d = await data.get()
#     yield d

class Boilerplate:
    def __init__(self, bot):
        self.bot = bot
        self.send = bot.send_message
        self.get = bot.get_message
        self.queue = asyncio.Queue()
        self.upd = bot.link + '/getUpdates'
        self.motd = Motd(API_KEY)

    async def feed(self, data):
        d = await data.get()
        yield d