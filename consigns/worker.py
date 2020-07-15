from newbot import Bot
import requests
import linecache
import sys
from consigns import consignment


class Worker(Bot, consignment.Civil, consignment.Currency, consignment.Consignment):

    @staticmethod
    def print_exception():
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

    def civil_add(self, data, consig):
        query = self.Civil.select().where(self.Civil.name == self.get_from_id(data))
        if query.exists():
            print('This Civil already exists')
        else:
            newciv = self.Civil(name=data, consignment=consig)
            newciv.save()

    def consign_add(self, name, color):
        query = self.Consignment.select().where(self.Consignment.name == name)
        if query.exists():
            print('This Consignment already exists')
        else:
            newconsign = self.Consignment(name=name, color=color)
            newconsign.save()

    def curr_add(self, consign, amount):
        query = self.Currency.update(balance=self.Currency.balance + amount).where(self.Currency.consignment == consign)
        query.execute()

    def delete_civ(self, data):
        check = self.Civil.select().where(self.Civil.name == data)
        if check.exists():
            query = self.Civil.delete().where(self.Civil.name == self.get_from_id(data))
            query.execute()
        else:
            print('This user is not in the Void')

    def list_all_civ(self):
        for i in self.Civil.select():
            print(f'Civil name: {i.name}, Civil consignment: {i.consignment}')

    def list_all_consig(self, *data):
        if data:
            try:
                with open('consig_list', 'r') as f:
                    r = f.read()
                    requests.post(self.send_message(), data=self.make_payload(self.get_chat_id(data), r))
            except Exception:
                self.print_exception()
        elif not data:
            for i in self.Consignment.select():
                print(f'Consign name: {i.name}, Consign color: {i.color}')

    def list_all_curr(self):
        for i in self.Currency.select():
            print(f'Consig: {i.consignment}, balance: {i.balance}')
