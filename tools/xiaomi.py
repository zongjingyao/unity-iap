#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import hashlib
import argparse
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client_id", help="UnityChannel Client ID")
    parser.add_argument("--client_secret", help="UnityChannel Client Secret")
    parser.add_argument("--public_key", help="UnityChannel Public Key")
    parser.add_argument("--verify_signature", action='store_true', help="Verfiy signature")
    parser.add_argument("--verify_api", action='store_true', help="Verfiy via server API")
    parser.add_argument("--receipt", help="Xiaomi IAP receipt")
    parser.add_argument("--debug", action='store_true', help="Use debug environment")
    args = parser.parse_args()

    if args.verify_signature and not args.public_key:
        print('\nPlease offer Public Key!')

    if args.verify_api and not (args.client_id and args.client_secret):
        print('\nPlease offer Client ID, Client Secret!')

    if not args.verify_signature and not args.verify_api:
        print('\nPlease specify a way to verify receipt! --verify_signature or --verify_api')

    if not args.receipt:
        print('\nPlease offer Xiaomi IAP receipt!')
        return

    xiaomi = Xiaomi(args.client_id, args.client_secret, args.public_key, args.verify_signature,
                    args.verify_api, args.debug)
    result = xiaomi.verify_receipt(args.receipt)
    print('\nThe receipt in %s environment is %s.\n' % \
        ('debug' if args.debug else 'production', 'valid' if result[0] else 'invalid'))
    if result[1]:
        print result[1]


if __name__ == '__main__':
    main()
