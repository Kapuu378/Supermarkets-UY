from context import *
import time

import requests

from requests.exceptions import ConnectionError, ConnectTimeout

class Client(requests.Session):
    def __init__(self):
        super().__init__()
        self.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8;charset=utf-8',
            'Accept-Language': 'es-AR,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Connection': 'keep-alive'
        })
    
    def request(self, method, url, params, *args, **kwargs):
        time.sleep(2.5)
        try:
            return super().request(method=method, url=url, params=params, *args, **kwargs)
        
        except (ConnectionError, ConnectTimeout):
            print("Connection was not estabilished succesfully.")
            time.sleep(60)
            return None
        
class VtexBaseScrapper():    
    client = Client()

    def __init__(self, base_url):
        self.base_url = base_url

    def _fetch(self, params) -> requests.Response | None:
        return self.client.get(url=self.base_url, params=params)
