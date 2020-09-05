from peewee import *
from newbot import Bot
import os

database = SqliteDatabase(f'{os.path.dirname(os.path.abspath(__file__))}/Database.db')


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class Notes(BaseModel):
    id = AutoField(column_name='Id', null=True)
    name = TextField(column_name='Name')
    text = TextField(column_name='Text')
    uid = IntegerField(column_name='Uid')

    class Meta:
        table_name = 'Notes'


class SqliteSequence(BaseModel):
    name = BareField(null=True)
    seq = BareField(null=True)

    class Meta:
        table_name = 'sqlite_sequence'
        primary_key = False


# database.create_tables([Notes, SqliteSequence])


class Worker(Notes, Bot):

    @staticmethod
    def list_all_notes():
        for i in Notes.select():
            print(f'Id: {i.id}, Name: {i.name}, Text: {i.text}, Uid: {i.uid}')

    async def add_note(self, name, text, uid, dirt=None):
        if dirt is not None:
            newnote = Notes(name=self.get_name(name), text=self.get_message(text), uid=self.get_from_id(uid))
            newnote.save()
        else:
            newnote = Notes(name=name, text=text, uid=uid)
            newnote.save()

    @staticmethod
    async def remove_by_id(_id):
        check = Notes.select().where(Notes.id == _id)
        if check.exists():
            query = Notes.delete().where(Notes.id == _id)
            query.execute()
        else:
            print('Note does not exist')

    def remove_by_name(self, name, dirt=None):
        if dirt is not None:
            check = Notes.select().where(Notes.name == self.get_name(name))
            if check.exists():
                query = Notes.delete().where(Notes.name == self.get_name(name))
                query.execute()
            else:
                print('Note does not exist')
        else:
            check = Notes.select().where(Notes.name == name)
            if check.exists():
                query = Notes.delete().where(Notes.name == name)
                query.execute()
            else:
                print('Note does not exist')

    def remove_by_text(self, text, dirt=None):
        if dirt is not None:
            check = Notes.select().where(Notes.text == self.get_message(text))
            if check.exists():
                query = Notes.delete().where(Notes.text == self.get_message(text))
                query.execute()
            else:
                print('Note does not exist')
        else:
            check = Notes.select().where(Notes.text == text)
            if check.exists():
                query = Notes.delete().where(Notes.text == text)
                query.execute()
            else:
                print('Note does not exist')

    def remove_by_uid(self, uid, dirt=None):
        if dirt is not None:
            check = Notes.select().where(Notes.uid == self.get_from_id(uid))
            if check.exists():
                query = Notes.delete().where(Notes.uid == self.get_from_id(uid))
                query.execute()
            else:
                print('Note does not exist')
        else:
            check = Notes.select().where(Notes.uid == uid)
            if check.exists():
                query = Notes.delete().where(Notes.uid == uid)
                query.execute()
            else:
                print('Note does not exist')

    @staticmethod
    def select_by_id(_id):
        query = Notes.select().where(Notes.id == _id)
        if query.exists():
            for i in query:
                print(f'Id: {i.id},Name: {i.name}, Text: {i.text}, Uid: {i.uid}')
        else:
            print('Note does not exist')

    def select_by_name(self, name, dirt=None):
        if dirt is not None:
            query = Notes.select().where(Notes.name == self.get_name(name))
            if query.exists():
                for i in query:
                    print(f'Id: {i.id},Name: {i.name}, Text: {i.text}, Uid: {i.uid}')
            else:
                print('Note does not exist')
        else:
            query = Notes.select().where(Notes.name == name)
            if query.exists():
                for i in query:
                    print(f'Id: {i.id},Name: {i.name}, Text: {i.text}, Uid: {i.uid}')
            else:
                print('Note does not exist')

    def select_by_text(self, text, dirt=None):
        if dirt is not None:
            query = Notes.select().where(Notes.text == self.get_message(text))
            if query.exists():
                for i in query:
                    print(f'Id: {i.id},Name: {i.name}, Text: {i.text}, Uid: {i.uid}')
            else:
                print('Note does not exist')
        else:
            query = Notes.select().where(Notes.text == text)
            if query.exists():
                for i in query:
                    print(f'Id: {i.id},Name: {i.name}, Text: {i.text}, Uid: {i.uid}')
            else:
                print('Note does not exist')

    def select_by_uid(self, uid, dirt=None):
        if dirt is not None:
            query = Notes.select().where(Notes.uid == self.get_from_id(uid))
            if query.exists():
                for i in query:
                    print(f'Id: {i.id},Name: {i.name}, Text: {i.text}, Uid: {i.uid}')
            else:
                print('Note does not exist')
        else:
            query = Notes.select().where(Notes.uid == uid)
            if query.exists():
                for i in query:
                    print(f'Id: {i.id},Name: {i.name}, Text: {i.text}, Uid: {i.uid}')
            else:
                print('Note does not exist')

    def select_all(self, _id=None, name=None, text=None, uid=None, dirt=None, uid_text=None):
        if _id is not None:
            all_fetched = {}
            query = Notes.select().where(Notes.id == _id)
            for i in query:
                fetched = {i.id: i.id}
                all_fetched.update(fetched)
            return all_fetched
        elif name is not None:
            if dirt is not None:
                all_fetched = {}
                query = Notes.select().where(Notes.name == self.get_name(name))
                for i in query:
                    fetched = {i.id: i.name}
                    all_fetched.update(fetched)
                return all_fetched
            else:
                all_fetched = {}
                query = Notes.select().where(Notes.name == name)
                for i in query:
                    fetched = {i.id: i.name}
                    all_fetched.update(fetched)
                return all_fetched
        elif text is not None:
            if dirt is not None:
                all_fetched = {}
                query = Notes.select().where(Notes.text == self.get_message(text))
                for i in query:
                    fetched = {i.id: i.text}
                    all_fetched.update(fetched)
                return all_fetched
            else:
                all_fetched = {}
                query = Notes.select().where(Notes.text == text)
                for i in query:
                    fetched = {i.id: i.text}
                    all_fetched.update(fetched)
                return all_fetched
        elif uid is not None:
            if dirt is not None:
                all_fetched = {}
                query = Notes.select().where(Notes.uid == self.get_from_id(uid))
                for i in query:
                    fetched = {i.id: i.uid}
                    all_fetched.update(fetched)
                return all_fetched
            else:
                all_fetched = {}
                query = Notes.select().where(Notes.uid == uid)
                for i in query:
                    fetched = {i.id: i.uid}
                    all_fetched.update(fetched)
                return all_fetched
        elif uid_text is not None:
            all_fetched = {}
            _id = 0
            query = Notes.select().where(Notes.uid == uid_text)
            for i in query:
                fetched = {_id: [i.uid, i.text]}
                all_fetched.update(fetched)
                _id += 1
            return all_fetched

    def list_text_uid(self, uid):
        collection = self.select_all(uid_text=uid)
        result = []
        for item in collection.items():
            iterated = item[1][1]
            result.append(iterated)
        return result
