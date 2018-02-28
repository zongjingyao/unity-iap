#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Validating Receipts With the App Store
https://developer.apple.com/library/content/releasenotes/General/ValidateAppStoreReceipt/Chapters/ValidateRemotely.html
'''
import json
import argparse
import requests


class Apple():
    NAME = 'AppleAppStore'
    URL_VERIFY_RECEIPT = 'https://buy.itunes.apple.com/verifyReceipt'
    SANDBOX_URL_VERIFY_RECEIPT = 'https://sandbox.itunes.apple.com/verifyReceipt'

    def __init__(self, shared_secret):
        self._shared_secret = shared_secret
        self._session = requests.session()

    def _send_request(self, url, receipt):
        data = json.dumps({'receipt-data': receipt, 'password': self._shared_secret})
        headers = {'Content-Type': 'text/plain'}
        return self._session.post(url=url, data=data, headers=headers)

    def verify_receipt(self, receipt):
        resp = self._send_request(Apple.URL_VERIFY_RECEIPT, receipt)
        json_data = resp.json()
        # 21007: This receipt is from the test environment, but it was sent to the production
        # environment for verification. Send it to the test environment instead.
        if 'status' in json_data and json_data['status'] == 21007:
            resp = self._send_request(Apple.SANDBOX_URL_VERIFY_RECEIPT, receipt)
            json_data = resp.json()
        if 'status' in json_data and json_data['status'] == 0:
            return (True, resp.content)
        return (False, resp.content)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--secret", help="Shared Secret")
    parser.add_argument("-r", "--receipt", help="Apple App Store IAP receipt")
    args = parser.parse_args()
    if not args.receipt:
        print('Please offer Apple App Store IAP receipt!')
        return
    apple = Apple(args.secret)
    result = apple.verify_receipt(args.receipt)
    print('\nThe receipt is %s.\n' % ('valid' if result[0] else 'invalid'))
    if result[1]:
        print (result[1])


if __name__ == '__main__':
    main()
