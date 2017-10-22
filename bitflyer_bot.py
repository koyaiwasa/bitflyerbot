# -*- coding: utf-8 -*-
import requests
import json, sys, time, hmac, hashlib

API_KEY = ""
API_SECRET = ""
BASE_URL = "https://api.bitflyer.jp{0}"

error_limit = 10


class BitflyerBot:

    api_key = ""
    api_secret = ""
    error_count = 0

    def __init__(self, api_key, api_secret):
        self.session = requests.session()
        self.api_key = api_key
        self.api_secret = api_secret

    # マーケットの一覧を取得
    def get_markets(self):
        response = self.get_request("/v1/getmarkets").json()
        print(response)

    # 板情報を取得
    def get_board(self, product_code: str=None):
        params = {"product_code": product_code}
        response = self.get_request("/v1/getboard", params=params).json()
        print(response)

    # Tickerを取得
    def get_ticker(self, product_code: str=None):
        params = {"product_code": product_code}
        response = self.get_request("/v1/getticker", params=params).json()
        print(response)

    # 約定履歴
    # TODO: before, afterの実装
    def get_executions(self, product_code: str=None):
        params = {"product_code": product_code}
        response = self.get_request("/v1/getexecutions", params=params).json()
        print(response)

    # 板の状態
    def get_board_state(self, product_code: str=None):
        params = {"product_code": product_code}
        response = self.get_request("/v1/getboardstate", params=params).json()
        print(response)

    # 取引所の状態
    def get_health(self, product_code: str=None):
        params = {"product_code": product_code}
        response = self.get_request("/v1/gethealth", params=params).json()
        print(response)

    # チャットの取得
    # TODO: from_dateの実装
    def get_chats(self, from_date: str=None):
        params = {}
        response = self.get_request("/v1/getchats", params=params).json()
        print(response)

    # APIキーの権限を取得
    def get_permissions(self):
        method = "GET"
        endpoint = "/v1/me/getpermissions"
        body = ""
        headers = self.create_private_header(method=method, endpoint=endpoint, body=body)
        response = self.get_request(endpoint=endpoint, params=body, headers=headers).json()
        print(response)

    # 資産残高を取得
    def get_balance(self):
        method = "GET"
        endpoint = "/v1/me/getbalance"
        body = ""
        headers = self.create_private_header(method=method, endpoint=endpoint, body=body)
        response = self.get_request(endpoint=endpoint, params=body, headers=headers).json()
        print(response)

    # 証拠金の状態を取得
    def get_collateral(self):
        method = "GET"
        endpoint = "/v1/me/getcollateral"
        body = ""
        headers = self.create_private_header(method=method, endpoint=endpoint, body=body)
        response = self.get_request(endpoint=endpoint, params=body, headers=headers).json()
        print(response)

    # 通貨別の証拠金の数量を取得
    def get_collateralaccounts(self):
        method = "GET"
        endpoint = "/v1/me/getcollateralaccounts"
        body = ""
        headers = self.create_private_header(method=method, endpoint=endpoint, body=body)
        response = self.get_request(endpoint=endpoint, params=body, headers=headers).json()
        print(response)

    # Private API用のヘッダーを作成
    def create_private_header(self, method, endpoint, body):
        if self.api_key and self.api_secret:
            access_timestamp = str(time.time())
            api_secret = str.encode(self.api_secret)
            text = str.encode(access_timestamp + method + endpoint + body)
            access_sign = hmac.new(api_secret,
                                   text,
                                   hashlib.sha256).hexdigest()
            auth_header = {
                "ACCESS-KEY": self.api_key,
                "ACCESS-TIMESTAMP": access_timestamp,
                "ACCESS-SIGN": access_sign,
                "Content-Type": "application/json"
            }
            return auth_header
        else:
            sys.exit()

    def get_request(self, endpoint, params=None, headers=None):
        url = BASE_URL.format(endpoint)
        while True:
            try:
                response = self.session.get(url, params=params, headers=headers)
                if not (response.status_code == 200 or response.status_code == 404):
                    continue
                self.error_count = 0
                return response
            except Exception as e:
                if self.error_count < error_limit:
                    self.error_count += 1
                    continue
                else:
                    sys.exit(e)

    def post_request(self, endpoint, params=None, headers=None):
        url = BASE_URL.format(endpoint)
        while True:
            try:
                response = self.session.post(url, data=params, headers=headers)
                if response.status_code != 200:
                    continue
                self.error_count = 0
                return response
            except Exception as e:
                if self.error_count < error_limit:
                    self.error_count += 1
                    continue
                else:
                    sys.exit(e)



if __name__ == "__main__":
    bitflyer_bot = BitflyerBot(api_key=API_KEY, api_secret=API_SECRET)
    bitflyer_bot.get_markets()
    bitflyer_bot.get_board("FX_BTC_JPY")
    bitflyer_bot.get_ticker("FX_BTC_JPY")
    bitflyer_bot.get_executions("FX_BTC_JPY")
    bitflyer_bot.get_board_state("FX_BTC_JPY")
    bitflyer_bot.get_health("FX_BTC_JPY")
    # bitflyer_bot.get_chats()
    bitflyer_bot.get_permissions()
    bitflyer_bot.get_balance()
    bitflyer_bot.get_collateral()
    bitflyer_bot.get_collateralaccounts()
