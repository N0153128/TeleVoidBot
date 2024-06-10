import logging
import os


class Loger:

    @staticmethod
    async def log_saver(name, uid, message, ctype, cid, uname):
        logging.basicConfig(filename=f'{os.path.dirname(os.path.abspath(__file__))}/../logs/general.log', level=logging.INFO,
                            format='%(asctime)s:%(message)s')
        logging.info('TYPE {}-{} BY @{}-{}, ID {} : {}'.format(ctype, cid, uname, name, uid, message))
