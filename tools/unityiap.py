#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
from google_play import GooglePlay
from apple import Apple
from xiaomi import Xiaomi


class UnityIAP():

    def __init__(self, config_path):
        with open(config_path) as config_file:
            config = json.load(config_file)
        xiaomi = config['xiaomi']
        self._xiaomi = Xiaomi(xiaomi['client_id'], xiaomi['client_secret'], xiaomi['public_key'],
                              xiaomi['verify_signature'], xiaomi['verify_api'], xiaomi['is_debug'])
        google_play = config['google_play']
        self._google_play = GooglePlay(google_play['public_key'])
        apple_app_store = config['apple_app_store']
        self._apple = Apple(apple_app_store['shared_secret'])

    def _verify_xiaomi_receipt(self, unified_receipt):
        payload = unified_receipt['Payload']
        return self._xiaomi.verify_receipt(payload)

    def _verify_google_play_receipt(self, unified_receipt):
        payload = unified_receipt['Payload']
        return self._google_play.verify_receipt(payload)

    def _verfiy_apple_app_store_receipt(self, unified_receipt):
        payload = unified_receipt['Payload']
        return self._apple.verify_receipt(payload)

    def verify_unified_receipt(self, unified_receipt):
        store = unified_receipt['Store']
        if store == Xiaomi.NAME:
            print(self._verify_xiaomi_receipt(unified_receipt)[0])
        elif store == GooglePlay.NAME:
            print(self._verify_google_play_receipt(unified_receipt)[0])
        elif store == Apple.NAME:
            print(self._verfiy_apple_app_store_receipt(unified_receipt)[0])


def main():
    unityiap = UnityIAP('./config.json')
    with open('./receipts.txt') as receipts:
        for receipt in receipts:
            unityiap.verify_unified_receipt(json.loads(receipt))


if __name__ == '__main__':
    main()