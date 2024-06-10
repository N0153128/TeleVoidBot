import time


class Spam:

    def __init__(self):
        self.watchlist = {}

    def checker(self, uid):
        if uid in self.watchlist:
            if int(time.time())-int(self.watchlist[uid]) < 3:
                self.watchlist.update({uid: int(time.time())})
                return False
            elif int(time.time())-int(self.watchlist[uid]) >= 3:
                self.watchlist.update({uid: int(time.time())})
                return True
        elif uid not in self.watchlist:
            self.watchlist.update({uid: int(time.time())})
            return True
