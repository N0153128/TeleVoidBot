# coding=utf8
from newbot import Bot
from tools import logmod
from mods import mods
import time
from consigns import consignment
from mods import teleworker
import asyncio
from multiprocessing import Process
import sys
from consigns import products

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
bot = Bot(token=sys.argv[1])
print(f'\nUsing token: {bot.token}\n')
mods = mods.Mods()
log = logmod.Loger()
# spam = spam.Spam()
worker = consignment.Worker(token=sys.argv[1])
teleworker = teleworker.Worker()
products = products.ProductsWorker()

# initializing variables
upd = bot.link + '/getUpdates'
queue = asyncio.Queue()
localtime = time.asctime(time.localtime(time.time()))
launchtime = time.time()

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
                if bot.get_callback_data(item) == 'communist':
                    await bot.callback_response(item, worker.id_to_curr(worker.name_to_id(bot.get_callback_data(item)),
                                                                        fore=True))
                elif bot.get_callback_data(item) == 'technocrat':
                    await bot.callback_response(item, worker.id_to_curr(worker.name_to_id(bot.get_callback_data(item)),
                                                                        fore=True))
                elif bot.get_callback_data(item) == 'liberal':
                    await bot.callback_response(item, worker.id_to_curr(worker.name_to_id(bot.get_callback_data(item)),
                                                                        fore=True))
                elif bot.get_callback_data(item) == 'conservative':
                    await bot.callback_response(item, worker.id_to_curr(worker.name_to_id(bot.get_callback_data(item)),
                                                                        fore=True))
                elif bot.get_callback_data(item) == 'lgbtqi++':
                    await bot.callback_response(item, worker.id_to_curr(worker.name_to_id(bot.get_callback_data(item)),
                                                                        fore=True))
                elif bot.get_callback_data(item) == 'koshkokraty':
                    await bot.callback_response(item, worker.id_to_curr(worker.name_to_id(bot.get_callback_data(item)),
                                                                        fore=True))

            # messages
            if bot.get_message(item) == '/void':
                await bot.send_message(item, 'Void')
            elif bot.get_message(item) == '/void@nUnionVoid_bot':
                await bot.send_message(item, 'Void')
            elif not bot.get_message(item):
                pass
            elif bot.get_message(item).startswith('/8ball'):
                if bot.get_from_id(item) == 237892260:
                    await bot.send_message(item, 'Yes')
                else:
                    await mods.ball(item)
            elif bot.get_message(item) == '/pic':
                await bot.send_photo(item, 'https://files.catbox.moe/ystpuu.jpg')
            elif bot.get_message(item) == '/uptime':
                await bot.get_uptime(launchtime, item)
            elif bot.get_message(item) == '/uptime@nUnionVoid_bot':
                await bot.get_uptime(launchtime, item)
            elif bot.get_message(item).startswith('/8ball@nUnionVoid_bot'):
                await mods.ball(item)
            elif bot.get_message(item).startswith('/rules'):
                if bot.get_chat_type(item) == 'private':
                    await mods.private_rules(item)
                elif bot.get_chat_type(item) == 'group':
                    await mods.group_rules(item)
            elif bot.get_message(item).startswith('/feedback'):
                await mods.feedback(item)
            elif bot.get_message(item).startswith('/tome'):
                await mods.save_locally(item)
            elif bot.get_message(item) == '/cat':
                await mods.cats(item)
            # RP
            elif bot.get_message(item) == '/pat':
                await mods.pat(item)
            elif bot.get_message(item) == '/hug':
                await mods.hug(item)
            elif bot.get_message(item) == '/le':
                await mods.le(item)
            elif bot.get_message(item) == '/kick':
                await mods.kick(item)
            elif bot.get_message(item) == '/swear':
                await mods.swear(item)
            elif bot.get_message(item) == '/angry':
                await mods.angry(item)
            # Telegraph
            elif bot.get_message(item).startswith('/save'):
                await mods.note_handler(item)
            elif bot.get_message(item) == '/showmine':
                await mods.send_keys(item)
            elif bot.get_message(item) == '/clear':
                await mods.clear(item)
            # Consignments
            elif bot.get_message(item) == '/list':
                await worker.send_all_consig(item)
            elif bot.get_message(item) == '/list@nUnionVoid_bot':
                await worker.send_all_consig(item)
            elif bot.get_message(item).startswith('/join'):
                await worker.civil_add(item, dirty=True)
            elif bot.get_message(item) == '/leave':
                await worker.delete_civ(item, dirty=True)
            elif bot.get_message(item) == '/leave@nUnionVoid_bot':
                await worker.delete_civ(item, dirty=True)
            elif bot.get_message(item) == '/balance':
                await worker.send_balance(item)
            elif bot.get_message(item) == '/balance@nUnionVoid_bot':
                await worker.send_balance(item)
            elif bot.get_message(item) == '/leaderboard':
                await worker.balance_leaderboard(item)
            elif bot.get_message(item) == '/leaderboard@nUnionVoid_bot':
                await worker.balance_leaderboard(item)
            # Exclusive
            elif bot.get_message(item) == '/showmeproducts':
                if bot.strict(item):
                    await bot.send_message(item, products.list_all_items())
                else:
                    await bot.send_message(item, 'Access denied')
            elif bot.get_message(item) == '/showmeconsigs':
                if bot.strict(item):
                    await bot.send_message(item, worker.list_all_consig(admin=True))
                else:
                    await bot.send_message(item, 'Access denied')
            elif bot.get_message(item) == '/showmecurr':
                if bot.strict(item):
                    await bot.send_message(item, worker.list_all_curr())
                else:
                    await bot.send_message(item, 'Access denied')
            elif bot.get_message(item) == '/showmeciv':
                if bot.strict(item):
                    await bot.send_message(item, worker.list_all_civ(admin=True))
                else:
                    await bot.send_message(item, 'Access denied')
            elif bot.get_message(item) == '/showmenotes':
                if bot.strict(item):
                    await bot.send_message(item, teleworker.list_text_for_admin())
                else:
                    await bot.send_message(item, 'Access denied')
            elif bot.get_message(item) == '/debug':
                await bot.send_message(item, 'Ебаный насос, жора, где ты был?\nХодил, гулял, курил...')

            # Products
            # # debug
            elif bot.get_message(item) == 'inline':
                await bot.send_message(item, 'Here is your inline: ', inline=['suka', 'pidor', 'gandon'],
                                       callback=True)
        except Exception as e:
            print(e)


prc2 = Process(target=worker.curr_loop, args=(worker.list_all_consig(fore=True), 10))
prc2.start()

loop = asyncio.get_event_loop()
loop.run_until_complete(putin(queue))

# starting processes that would check for new messages and start adding currency for the consignments
