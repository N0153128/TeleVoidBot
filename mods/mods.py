import random
from newbot import Bot
from telegraph import Telegraph
import re
import time
from . import teleworker


class Mods(teleworker.Worker):

    def __init__(self):
        super().__init__()
        self.tph = Telegraph()
        self.bot = Bot()

    # /8ball method
    async def ball(self, data):
        vari = ['Yes', 'No', 'Maybe', 'NOOOOOOOO', 'YESSSSSSS',
                'Fuck you', 'suka', 'Not today', 'Not now', 'Ask me later', 'Ask Gargoyle']
        ans = random.choice(vari)
        await self.bot.send_message(data, ans, get_chat=True)

    # saves notes to the database
    async def note_saver(self, content, name, uid, data):
        title = 'ARTICLE BY VOID FOLLOWER'
        self.tph.create_account(short_name='Void_Follower')
        response = self.tph.create_page(title, html_content=content)
        await self.add_note(name, response['path'].strip('/save'), uid)
        dat = f"https://telegra.ph/{response['path']}"
        await self.bot.send_message(data, dat, get_chat=True)
        # TODO: add telegraph exception error handlers
        return True

    # displays user's notes
    async def note_serve(self, uid, dat):
        collection = self.list_text_uid(uid)
        if not collection:
            await self.bot.send_message(dat, 'Sorry m8, no cookies for you')
            await self.bot.delete_message(dat)
        else:
            for i in collection:
                data = 'https://telegra.ph/{}'.format(i)
                await self.bot.send_message(dat, data)

    # this method decides, whether it should save the note or throw an error message
    async def note_handler(self, item):
        data = self.bot.get_message(item)[5:]
        if len(data) > 5:
            if '@nUnionVoid_bot' in data:
                data = data.replace('@nUnionVoid_bot', 'New Union: ')
                if len(data) > 30:
                    if '<' in data:
                        redata = re.sub('[<>]', '', data)
                        await self.note_saver(redata, self.bot.get_name(item), self.bot.get_from_id(item), item)
                    else:
                        await self.note_saver(data, self.bot.get_name(item), self.bot.get_from_id(item), item)
                else:
                    await self.bot.send_message(item, 'Your message cannot be saved due to its short length',
                                                get_chat=True)
                    await self.bot.delete_message(item)
            else:
                if len(data) > 30:
                    if '<' in data:
                        redata = re.sub('[<>]', '', data)
                        await self.note_saver(redata, self.bot.get_name(item), self.bot.get_from_id(item), item)
                    else:
                        await self.note_saver(data, self.bot.get_name(item), self.bot.get_from_id(item), item)
                else:
                    await self.bot.send_message(item, 'Your message cannot be saved due to its short length',
                                                get_chat=True)
                    await self.bot.delete_message(item)
        else:
            await self.bot.send_message(item, 'Your message cannot be saved due to its short length', get_chat=True)
            await self.bot.delete_message(item)

    # /rules for group chats
    async def group_rules(self, data):
        with open('assets/group_rules', 'r+') as f:
            r = f.read()
            await self.bot.send_message(data, r, get_chat=True)
        return True

    # /rules for private chats
    async def private_rules(self, data):
        with open('assets/private_rules', 'r+') as f:
            r = f.read()
            await self.bot.send_message(data, r)
        return True

    # /feedback - sends user's message to separate account
    async def feedback(self, data):
        redata = self.bot.get_message(data)[9:]
        if len(redata) > 30:
            await self.bot.send_message('505811653', f'from: {self.bot.get_name(data)}, at: {time.time()}, '
                                                     f'id: {self.bot.get_from_id(data)}, '
                                                     f'text: {redata}', pure=True)
            await self.bot.send_message(data, 'Thank you for your feedback!', get_chat=True)
        else:
            await self.bot.send_message(data, 'Your feedback cannot be sent due to its short length', get_chat=True)
            await self.bot.delete_message(data)

    # /tome - sends user's message back to himself
    async def save_locally(self, data):
        redata = self.bot.get_message(data)[5:]
        if len(redata) > 5:
            await self.bot.send_message(data, redata)
        else:
            await self.bot.send_message(data, 'Your message cannot be saved due to its short length', get_chat=True)
            await self.bot.delete_message(data)

    # /cat - requests for cats help
    async def cats(self, data):
        if self.bot.get_chat_id(data) == -385389138:
            await self.bot.send_message(data, '@Karasten, Новый Союз нуждается в твоей кошачьей поддержке!',
                                        get_chat=True)
        else:
            await self.bot.delete_message(data)

    # /pat - appreciates cats help
    async def pat(self, data):
        if self.bot.get_chat_id(data) == -385389138:
            await self.bot.send_message(data, f'@Karasten, {self.bot.get_name(data)} гладит тебя по спинке',
                                        get_chat=True)
        else:
            await self.bot.delete_message(data)

    # /showmine - returns set of fancy keys with the links for user's notes
    async def send_keys(self, data):
        collection = self.list_text_uid(self.bot.get_from_id(data))
        await self.bot.send_message(data, 'this is all your notes so far: ', inline=collection)

    # /clear - clears user's notes
    async def clear(self, data):
        user_uid = self.bot.get_from_id(data)
        self.remove_by_uid(user_uid)
        await self.bot.send_message(data, 'Your text has been removed successfully', get_chat=True)
