#!/usr/bin/env python
# -*- coding:utf-8 -*-

import base64
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA


class Utils():

    @staticmethod
    def verify_signature(public_key, data, signature):
        key = RSA.importKey(public_key)
        missing_padding = 4 - len(signature) % 4
        if missing_padding:
            signature += '=' * missing_padding
        h = SHA.new(data.encode('utf-8'))
        verifier = PKCS1_v1_5.new(key)
        return verifier.verify(h, base64.b64decode(signature))
