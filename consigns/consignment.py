from peewee import *
import peewee
from newbot import Bot
import linecache
import sys
from statistics import mode
import statistics
from time import sleep
import os

db = SqliteDatabase(f'{os.path.dirname(os.path.abspath(__file__))}/../memory.db', autoconnect=True)
print(f'{os.path.dirname(os.path.abspath(__file__))}/../memory.db')


class Consignment(Model):
    name = CharField()
    color = CharField()

    class Meta:
        database = db


class Currency(Model):
    consignment = ForeignKeyField(Consignment, backref='currency')
    balance = IntegerField()

    class Meta:
        database = db


class Civil(Model):
    name = IntegerField()
    consignment = ForeignKeyField(Consignment, backref='civil')

    class Meta:
        database = db


db.create_tables([Civil, Currency, Consignment])


class Worker(Bot):

    # Debug method, used to determine errors with try/except block
    @staticmethod
    def print_exception():
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        line_no = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, line_no, f.f_globals)
        print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, line_no, line.strip(), exc_obj))

    # checks if the consignment that user entered exists
    async def consig_in_check(self, data):
        user_data = self.get_message(data)
        if user_data[6:].startswith('neon'):
            return 2
        elif user_data[6:].startswith('red'):
            return 1
        elif user_data[6:].startswith('yellow'):
            return 3
        elif user_data[6:].startswith('blue'):
            return 4
        elif user_data[6:].startswith('rainbow'):
            return 5
        elif user_data[6:].startswith('fluffy'):
            return 6
        else:
            await self.send_message(data, 'Invalid consignment colour', get_chat=True)
            return False

    @staticmethod
    def id_to_name(id_):
        try:
            query = Consignment[id_]
            return query.name
        except peewee.DoesNotExist:
            return False

    @staticmethod
    def name_to_id(name):
        try:
            query = Consignment.get(Consignment.name == name)
            return query.id
        except peewee.DoesNotExist:
            return False

    @staticmethod
    def id_to_curr(id_, fore=None):
        if fore is None:
            try:
                query = Currency[id_]
                return query.balance
            except peewee.DoesNotExist:
                return False
        elif fore is not None:
            try:
                query = Currency[id_]
                return f'Consignment\'s balance: {query.balance}'
            except peewee.DoesNotExist:
                return False

    # adds civil to the database
    async def civil_add(self, data, dirty=None):
        if not dirty:
            query = Civil.select().where(Civil.name == data)
            if query.exists():
                print('This Civil already exists')
            else:
                if await self.consig_in_check(data):
                    consig = await self.consig_in_check(data)
                    newciv = Civil(name=data, consignment=consig)
                    newciv.save()
        elif dirty is not None:
            query = Civil.select().where(Civil.name == self.get_from_id(data))
            if query.exists():
                print('This Civil already exists')
                await self.send_message(data, 'You\'re already member of a consignment', get_chat=True)
            else:
                if await self.consig_in_check(data):
                    consig = await self.consig_in_check(data)
                    newciv = Civil(name=self.get_from_id(data), consignment=consig)
                    newciv.save()
                    await self.send_message(data,
                                            f'Congrats! You\'ve just joined {self.get_message(data)[6:]} consignment',
                                            get_chat=True)

    # adds consignment to the database
    @staticmethod
    def consig_add(name, color):
        query = Consignment.select().where(Consignment.name == name)
        if query.exists():
            print('This Consignment already exists')
        else:
            newconsign = Consignment(name=name, color=color)
            newconsign.save()

    # gets leading consignment. leading consignment is determined by the amount of users that it has (more = better)
    @staticmethod
    def get_leader(data):
        try:
            if not data:
                pass
            else:
                return mode(data)
        except statistics.StatisticsError:
            pass

    # adds currency for the consignment.
    @staticmethod
    def curr_add(consign, amount):  # both consign and amount are integers
        check = Currency.select().where(Currency.consignment == consign)
        if check.exists():
            query = Currency.update(balance=Currency.balance + amount).where(Currency.consignment == consign)
            query.execute()
        else:
            query = Currency(consignment=consign, balance=amount)
            query.save()

    # adds currency for the consignment in infinite loop. leading consignment gets bonus of x1.5
    def curr_loop(self, consig, amount):
        while True:
            for i in consig:
                if i == self.get_leader(self.list_all_civ(fore=True)):
                    self.curr_add(i, amount * 1.5)
                # elif i == 1:
                #     self.curr_add(i, amount * 100000)
                else:
                    self.curr_add(i, amount)
            sleep(3)

    async def delete_civ(self, data, dirty=None):
        if not dirty:
            check = Civil.select().where(Civil.name == data)
            if check.exists():
                query = Civil.delete().where(Civil.name == data)
                query.execute()
            else:
                print('This user is not in the Void')
        elif dirty is not None:
            check = Civil.select().where(Civil.name == self.get_from_id(data))
            if check.exists():
                query = Civil.delete().where(Civil.name == self.get_from_id(data))
                query.execute()
                await self.send_message(data, 'You\'ve successfully left your consignment', get_chat=True)
            else:
                await self.send_message(data, 'You are not in the void', get_chat=True)

    # lists all civilians
    @staticmethod
    def list_all_civ(fore=None):
        amount = []
        if not fore:
            for i in Civil.select().dicts():
                civ = i
                amount.append(civ)
            return amount
        elif fore is not None:
            for i in Civil.select().dicts():
                civ = i['consignment']
                amount.append(civ)
            return amount

    # clears currency table
    @staticmethod
    def clear_curr():
        for i in Currency.select():
            query = i.delete()
            query.execute()

    # lists all consignments. returns a list with id, name and color, or only id
    @staticmethod
    def list_all_consig(fore=None):
        all_ = []
        if fore is None:
            for i in Consignment.select():
                consig = [i.id, i.name, i.color]
                all_.append(consig)
            return all_
        elif fore is not None:
            for i in Consignment.select():
                consig = i.id
                all_.append(consig)
            return all_

    # sends list of all consignments to the user
    async def send_all_consig(self, data):
        with open(f'{os.path.dirname(os.path.abspath(__file__))}/../assets/consig_list', 'r') as f:
            r = f.read()
            await self.send_message(data, r, get_chat=True)

    # shows consignment's balance to the user
    async def send_balance(self, data):
        query = Civil.select().where(Civil.name == self.get_from_id(data))
        if query.exists():
            get = Civil.get(Civil.name == self.get_from_id(data))
            get_curr = Currency.get(Currency.consignment == get.consignment)
            await self.send_message(data, f'Your consignment\'s balance: {get_curr.balance}', get_chat=True)
        elif not query.exists():
            await self.send_message(data, 'You are not in the void', get_chat=True)

    # lists all consignments and their balances
    @staticmethod
    def list_all_curr():
        for i in Currency.select():
            print(f'Consig: {i.consignment}, balance: {i.balance}')

    async def balance_leaderboard(self, data):
        leaderboard = []
        for i in Currency.select().order_by(Currency.balance.desc()):
            participant = self.id_to_name(i.id)
            leaderboard.append(participant)
        await self.send_message(data, 'This is consignments leaderboard', inline=leaderboard, callback=leaderboard)

    # DEBUG: checks if database connection is closed
    @staticmethod
    def is_closed():
        print(db.is_closed())

    # DEBUG: closes connection with the database
    @staticmethod
    def close_db():
        print(db.close())

    # DEBUG: prints list of all tables
    @staticmethod
    def get_tables():
        base = SqliteDatabase('memory.db')
        print(base.get_tables())

    # DEBUG: shows columns and their specifications for the table, that is given by an argument
    @staticmethod
    def get_cols(table):  # string
        base = SqliteDatabase(database='memory.db')
        print(base.get_columns(table))

