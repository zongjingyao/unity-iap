#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import argparse
from utils import Utils


class GooglePlay():
    NAME = 'GooglePlay'

    def __init__(self, public_key):
        self._public_key = '-----BEGIN PUBLIC KEY-----\n%s\n-----END PUBLIC KEY-----' % public_key

    def verify_receipt(self, receipt):
        receipt = json.loads(receipt)
        data = receipt['json']
        signature = receipt['signature']
        return (Utils.verify_signature(self._public_key, data, signature), None)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--public_key", help="Google License Key(Public Key)")
    parser.add_argument("-r", "--receipt", help="Google Play IAP receipt")
    args = parser.parse_args()
    if not args.public_key:
        print('Please offer Google License Key(Public Key)!')
        return
    if not args.receipt:
        print('Please offer Google Play IAP receipt!')
        return
    google_play = GooglePlay(args.public_key)
    result = google_play.verify_receipt(args.receipt)
    print('\nThe receipt is %s.\n' % ('valid' if result[0] else 'invalid'))
    if result[1]:
        print (result[1])


if __name__ == '__main__':
    main()
