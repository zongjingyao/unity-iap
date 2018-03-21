#!/usr/bin/env python
# -*- coding:utf-8 -*-

from os import path
import logging
import json
from flask import Flask, request, abort
app = Flask(__name__)

logger = logging.getLogger('Xiaomi')
logger.setLevel(level=logging.INFO)
log_path = path.abspath(path.join(path.dirname(__file__), './xiaomi.txt'))
handler = logging.FileHandler(log_path)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(handler)
logger.addHandler(console)
logger.info('=' * 50)
logger.info('Xiaomi log: %s' % log_path)


@app.route('/xiaomi', methods=['GET'])
def xiaomi():
    logger.info('new request: \n' + json.dumps(request.args))
    sign_data = request.args.get('signData', '')
    signature = request.args.get('signature', '')
    if not sign_data or not signature:
        logger.error('no signData or signature')
        abort(400, 'no signData or signature')
    logger.info('signData:\n%s' % sign_data)
    logger.info('signature:\n%s' % signature)
    return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
