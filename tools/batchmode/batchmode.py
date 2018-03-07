#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
from os import path
import subprocess
import logging

logger = logging.getLogger('BatchMode')
logger.setLevel(level=logging.INFO)
log_path = path.abspath(path.join(path.dirname(__file__), './log.txt'))
handler = logging.FileHandler(log_path)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(handler)
logger.addHandler(console)
logger.info('=' * 50)
logger.info('BatchMode log: %s' % log_path)


class BatchMode():

    def __init__(self, config_path):
        logger.info('Init BatchMode with config file: %s' % config_path)
        with open(config_path) as config_file:
            config = json.load(config_file)
            self._default = config['default']
            self._projects = config['projects']

    def build(self):
        for project in self._projects:
            cmds = ['-batchmode', '-quit']
            args = dict(self._default, **project)
            cmds.insert(0, args.pop('unityPath'))
            for k, v in args.items():
                cmds.append('-' + k)
                cmds.append(v)
            logger.info('*' * 50)
            logger.info('Begin build with cmd: \n\t' + ' '.join(cmds))
            ret_code = subprocess.call(cmds, shell=False)
            if ret_code == 0:
                logger.info('Done. Return code: %d.\n\tlog file: %s\n\tapk path:%s' %
                            (ret_code, args['logFile'], args['apkPath']))
            else:
                logger.error('Failed. Return code: %d.\n\tPlease check the log: %s' %
                             (ret_code, args['logFile']))


def main():
    batchmode = BatchMode(path.abspath(path.join(path.dirname(__file__), './config.json')))
    batchmode.build()


if __name__ == '__main__':
    main()
