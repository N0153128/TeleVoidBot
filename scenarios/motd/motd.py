import git
from typing import Dict, List, Optional
from pytonapi.schema.rates import Rates
from pytonapi.tonapi import TonapiClient
from pytonapi import Tonapi
from config import *
import json
import asyncio

class Motd(TonapiClient):
    def __init__(self, api_key: str, is_testnet: bool | None = False, max_retries: int | None = None, base_url: str | None = None, headers: Dict[str, any] | None = None, timeout: float | None = None) -> None:
        super().__init__(api_key, is_testnet, max_retries, base_url, headers, timeout)
        
        self.rates_obj = self.get_prices(tokens=['TON', 'EQBCFwW8uFUh-amdRmNY9NyeDEaeDYXd9ggJGsicpqVcHq7B'], currencies=['TON', 'GBP'])
        self.rates_json = json.loads(self.rates_obj.json())
        self.gbp_rate = self.rates_json['rates']['TON']['prices']['GBP']
        self.balance = self.get_balance()

    def get_git_commits(self, path):
        repo = git.Repo(path)
        return repo.git.rev_list('--count', 'HEAD')
    

    def get_balance(self, ):
        # Creating new Tonapi object
        tonapi = Tonapi(api_key=API_KEY)
        account = tonapi.accounts.get_info(account_id=ACCOUNT_ID)
        return account.balance.to_amount()
    
    def get_prices(self, tokens: List[str], currencies: List[str]) -> Rates:
        params = {
            'tokens': ','.join(map(str, tokens)),
            'currencies': ','.join(map(str, currencies)),
        }
        method = f"v2/rates"
        response = self._get(method=method, params=params)

        return Rates(**response)
    
    def get_payload(self):
        # print(f'Commits for Void Bot: {motd.get_git_commits(VOID_BOT)}')
        # print(f'Commits for ALTNET: {motd.get_git_commits(ALTNET)}')
        # print(f'Commits for DigiRunner: {motd.get_git_commits(DIGIRUNNER)}')
        # print(f'Commits for N0153.tech: {motd.get_git_commits(N0153WEB)}\n')
        # print(f'Ton balance: {motd.balance}')
        # print(f'Ton Pirce: {round(motd.gbp_rate, 2)}')
        # print(f'current balance: {round(motd.balance*motd.gbp_rate, 2)}')
        payload = f'''
            24 have passed, wake up.
            Current Weather:
            # Highest temperature today: 
            # Rain possibility:

            Ton coins holding: {motd.balance}
            Ton Pirce: {round(motd.gbp_rate, 2)}
            current balance: {round(motd.balance*motd.gbp_rate, 2)}

            Commits for Void Bot: {motd.get_git_commits(VOID_BOT)}
            Commits for ALTNET: {motd.get_git_commits(ALTNET)}
            Commits for DigiRunner: {motd.get_git_commits(DIGIRUNNER)}
            Commits for N0153.tech: {motd.get_git_commits(N0153WEB)}\n

            Unread emails: 

            Ton difference: (24h)

            '''

        return payload


    async def begin_push(self, item):
        while True:
            payload = self.get_payload()
            await self.send_message(item, message=payload)
            asyncio.sleep(3)

