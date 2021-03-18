import sys
import http.client
import urllib
import json
import hashlib
import hmac
import time
import requests


def get_api_keys(key, secret):
    keys = [key, secret]
    return keys



class ExmoAPI:
    def __init__(self, API_URL='api.exmo.me',
                 API_VERSION='v1.1'):
        self.keys = get_api_keys()
        self.API_URL = API_URL
        self.API_VERSION = API_VERSION
        self.API_KEY = self.keys[0]
        self.API_SECRET = bytes(self.keys[1], encoding='utf-8')

    def sha512(self, data):
        H = hmac.new(key=self.API_SECRET, digestmod=hashlib.sha512)
        H.update(data.encode('utf-8'))
        return H.hexdigest()

    def api_query(self, api_method, params=None):
        if params is None:
            params = {}
        params['nonce'] = int(round(time.time() * 1000))
        params = urllib.parse.urlencode(params)

        sign = self.sha512(params)
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Key": self.API_KEY,
            "Sign": sign,
            'User-Agent': 'Exmo_Bot'
        }
        conn = http.client.HTTPSConnection(self.API_URL)
        conn.request("POST", "/" + self.API_VERSION + "/" + api_method,
                     params, headers)
        response = conn.getresponse().read()

        conn.close()

        try:
            obj = json.loads(response.decode('utf-8'))
            if 'error' in obj and obj['error']:
                print(obj['error'])
                raise sys.exit()
            return obj
        except json.decoder.JSONDecodeError:
            print('Error while parsing response:', response)
            raise sys.exit()


# Получаем данные о текущих сделках и стаканах
def get_ticker(pair):
    url_trades = 'https://api.exmo.me/v1.1/ticker/'
    ticker = requests.get(url_trades)
    info = ticker.text
    info = json.loads(info)
    info_pair = info.get(pair)
    return info_pair

    # Получаем содержимое кошелька по паре


def get_wallet(pair, api_key, api_secret_key):
    EXMO_K = api_key
    EXMO_S = api_secret_key
    ExmoAPI_instance = ExmoAPI(EXMO_K, EXMO_S)
    info = ExmoAPI_instance.api_query('user_info')

    pair_wallets = info.get('balances')
    pair_name = pair.split('_')
    pair_wallet = pair_wallets.get(pair_name[0])
    return (pair_name[0], pair_wallet)


def get_pairs():
    url = "https://api.exmo.com/v1.1/pair_settings"



