import requests
import urllib3
import time
from context import *
from .validate import validate_request
from requests.exceptions import JSONDecodeError, ConnectionError, ConnectTimeout

class Client(requests.Session):
    def __init__(self):
        super().__init__()
        self.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'es-AR,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Connection': 'keep-alive'
        })
    
    def request(self, *args, **kwargs):
        time.sleep(2.5)
        try:
            return super().request(*args, **kwargs)
        
        except (ConnectionError, ConnectTimeout):
            print("Connection was not estabilished succesfully.")
            time.sleep(60)
            return None