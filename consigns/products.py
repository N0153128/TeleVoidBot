import peewee
from peewee import *
import os

db = SqliteDatabase(f'{os.path.dirname(os.path.abspath(__file__))}/../items.db', autoconnect=True)
print(f'{os.path.dirname(os.path.abspath(__file__))}/../memory.db')


# regular items class, contains items, that could be purchased by any player
class RegItems(Model):
    name = CharField()
    max_allowed = IntegerField()
    quality = BooleanField()

    class Meta:
        database = db


class Owners(Model):
    name = CharField()
    item = ForeignKeyField(RegItems, backref='owner')
    quantity = IntegerField()

    class Meta:
        database = db


db.create_tables([RegItems, Owners])


class Worker:

    @staticmethod
    def item_add(name, maxal, quality):
        query = RegItems.select().where(RegItems.name == name)
        if query.exists():
            print('This item already exists')
        else:
            newitem = RegItems(name=name, max_allowed=maxal, quality=quality)
            newitem.save()

    @staticmethod
    def delete_item(name):
        check = RegItems.select().where(RegItems.name == name)
        if check.exists():
            query = RegItems.delete().where(RegItems.name == name)
            query.execute()
        else:
            print('This item is not in the void')

    @staticmethod
    def if_item_exists(name):
        check = RegItems.select().where(RegItems.name == name)
        if check.exists():
            return True
        else:
            return False

    @staticmethod
    def list_all_items():
        query = RegItems.select()
        try:
            for i in query:
                print(f'Item name: {i.name}, Maximum allowed: {i.max_allowed}, Quality: {i.quality}')
        except Exception as e:
            print(e)

    @staticmethod
    def drop_items():
        for i in RegItems.select():
            query = i.delete()
            query.execute()


# DEBUG: checks if database connection is closed
def is_closed():
    print(db.is_closed())


# DEBUG: closes connection with the database
def close_db():
    print(db.close())


# DEBUG: prints list of all tables
def get_tables():
    base = SqliteDatabase('items.db')
    print(base.get_tables())


# DEBUG: shows columns and their specifications for the table, that is given by an argument
def get_cols(table):  # string
    base = SqliteDatabase(database='items.db')
    print(base.get_columns(table))
