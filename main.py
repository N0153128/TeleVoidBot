from newbot import Bot
from tools import logmod
from mods import mods
import time
from consigns import consignment
from mods import teleworker
import asyncio
from multiprocessing import Process

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
bot = Bot()
mods = mods.Mods()
log = logmod.Loger()
# spam = spam.Spam()
worker = consignment.Worker()
teleworker = teleworker.Worker()

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
                                bot.get_chat_type(data), bot.get_chat_id(data), bot.get_username(data))
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
                await bot.send_message(item, 'Void', get_chat=True, )
            elif bot.get_message(item) == '/void@nUnionVoid_bot':
                await bot.send_message(item, 'Void', get_chat=True)
            elif not bot.get_message(item):
                pass
            elif bot.get_message(item).startswith('/8ball'):
                await mods.ball(item)
            elif bot.get_message(item).startswith('/8ball@nUnionVoid_bot'):
                await mods.ball(item)
            elif bot.get_message(item).startswith('/save'):
                await mods.note_handler(item)
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
            elif bot.get_message(item) == '/pat':
                await mods.pat(item)
            elif bot.get_message(item) == '/showmine':
                await mods.send_keys(item)
            elif bot.get_message(item) == '/clear':
                await mods.clear(item)
            # # Consignments
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

# DEBUG: sample of json object
dump = {"ok": True, "result": [{"update_id": 963774730,
                                "message": {"message_id": 7771,
                                            "from": {"id": 237892260, "is_bot": False, "first_name": "N0153",
                                                     "username": "noisebro", "language_code": "en"},
                                            "chat": {"id": 237892260, "first_name": "N0153", "username": "noisebro",
                                                     "type": "private"}, "date": 1585682799,
                                            "text": "\u041f\u0440\u0438\u0432\u0435\u0442"}}]}
dump1 = {"ok": True, "result": [{"update_id": 963775083,
                                 "callback_query": {"id": "1021739479273566550",
                                                    "from": {"id": 237892260, "is_bot": False, "first_name": "N0153",
                                                             "username": "noisebro", "language_code": "en"},
                                                    "message": {"message_id": 8248,
                                                                "from": {"id": 1032150163, "is_bot": True,
                                                                         "first_name": "Void",
                                                                         "username": "nUnionVoid_bot"},
                                                                "chat": {"id": 237892260, "first_name": "N0153",
                                                                         "username": "noisebro", "type": "private"},
                                                                "date": 1586120963, "text": "Here is your inline:",
                                                                "reply_markup": {"inline_keyboard": [[{"text": "suka",
                                                                                                       "callback_data": "callback_data0"}],
                                                                                                     [{"text": "pidor",
                                                                                                       "callback_data": "callback_data1"}],
                                                                                                     [{"text": "gandon",
                                                                                                       "callback_data": "callback_data2"}]]}},
                                                    "chat_instance": "3976568242328110719", "data": "callback_data0"}}]}
