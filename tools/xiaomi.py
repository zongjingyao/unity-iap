#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import hashlib
import requests
from utils import Utils


class Xiaomi():
    NAME = 'XiaomiMiPay'
    DEBUG_URL_VERIFY_RECEIPT = 'https://cn-api-debug.unity.com/v1/order-attempts/query'
    DEBUG_URL_VERIFY_LOGIN = 'https://cn-api-debug.unity.com/v1/login-attempts/verifyLogin'
    URL_VERIFY_RECEIPT = 'https://cn-api.unity.com/v1/order-attempts/query'
    URL_VERIFY_LOGIN = 'https://cn-api.unity.com/v1/login-attempts/verifyLogin'

    def __init__(self, client_id, client_secret, public_key, verify_signature, verify_api,
                 is_debug):
        self._client_id = client_id
        self._client_secret = client_secret
        self._public_key = '-----BEGIN PUBLIC KEY-----\n%s\n-----END PUBLIC KEY-----' % public_key
        self._verify_signature = verify_signature
        self._verify_api = verify_api
        self._is_debug = is_debug
        self._session = requests.session()

    def verify_receipt(self, receipt):
        receipt = json.loads(receipt)
        if self._verify_signature:
            data = receipt['json']
            signature = receipt['signature']
            if Utils.verify_signature(self._public_key, data, signature):
                return (True, None)
        if self._verify_api:
            cp_order_id = receipt['gameOrderId']  #gameOrderId IS cpOrderId
            order_query_token = receipt['orderQueryToken']
            sign_data = '%s&%s&%s&%s' % (self._client_id, cp_order_id, order_query_token,
                                         self._client_secret)
            sign = hashlib.md5(sign_data).hexdigest()
            params = {
                'cpOrderId': cp_order_id,
                'clientId': self._client_id,
                'orderQueryToken': order_query_token,
                'sign': sign
            }
            url = Xiaomi.DEBUG_URL_VERIFY_RECEIPT if self._is_debug else Xiaomi.URL_VERIFY_RECEIPT
            resp = self._session.get(url=url, params=params)
            json_data = resp.json()
            if json_data.has_key('status') and json_data['status'] == 'SUCCESS':
                return (True, resp.content)
        return (False, None)

    def verify_login(self, user_login_token):
        sign_data = '%s&%s' % (user_login_token, self._client_secret)
        sign = hashlib.md5(sign_data).hexdigest()
        url = Xiaomi.DEBUG_URL_VERIFY_LOGIN if self._is_debug else Xiaomi.URL_VERIFY_LOGIN
        params = {'userLoginToken': user_login_token, 'sign': sign}
        resp = self._session.get(url=url, params=params)
        return resp.content
