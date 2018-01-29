#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
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
