
from initial import *


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
                    if get(item) in motd_commands:
                        await motd_handler(item)
                    else:
                        await command_cycle(item)
            elif not admin:
                  await command_cycle(item)

        except Exception as e:
            print(e)

async def command_cycle(data):
    if get(data) == '/debug':
        await send(data, 'Ping')
    elif get(data).startswith('/bal'):
        pass
        # await send(data, motd.balance)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(bot.loop_void(queue=queue, data_resolver=motd_handler))

loop2 = asyncio.get_event_loop()
loop2.create_task(bot.loop_void(queue=queue, data_resolver=webapi_handler))
loop2.run_forever()

