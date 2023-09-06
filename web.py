import requests
from newbot import Bot
import webcreds
from requests.auth import HTTPBasicAuth

class RestfulInteract:

    @staticmethod
    def post(title, text):
        url = 'https://n0153.tech/apipost/'
        auth = HTTPBasicAuth(webcreds.USERNAME, webcreds.PASSWORD)
        payload = {
            'post_title': title,
            'post_text': text,
        }
        resp = requests.post(url=url, data=payload, auth=auth)
    def get_data(self, data):
        title = data.split('|')[0]
        title = title[6:-1]
        text = data.split('|')[1]
        return title, text