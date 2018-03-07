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
                logger.info('Done. Return code: %d.\n\tlog file: %s\n\tapk path: %s' %
                            (ret_code, args['logFile'], args['apkPath']))
            else:
                logger.error('Failed. Return code: %d.\n\tPlease check the log: %s' %
                             (ret_code, args['logFile']))

    def create_project(self, project):
        logger.error('Create project at ' + project['projectPath'])
        if path.exists(project['projectPath']):
            logger.error('Project has already been existing!')
            return
        # create project
        cmds = [
            self._default['unityPath'], '-batchmode', '-quit', '-logFile',
            project['logFile'], '-createProject', project['projectPath']
        ]
        logger.info('Create project with cmd: \n\t' + ' '.join(cmds))
        ret_code = subprocess.call(cmds, shell=False)
        if ret_code == 0:
            logger.info('Done. Return code: %d.\n\tlog file: %s' % (ret_code, project['logFile']))
        else:
            logger.error('Failed. Return code: %d.\n\tPlease check the log: %s' % (ret_code, 
                project['logFile']))

    def import_package(self, project, package_path):
        cmds = [
            self._default['unityPath'], '-projectPath', project['projectPath'], '-logFile',
            project['logFile'], '-importPackage', package_path)
        ]
        logger.info('Import package with cmd: \n\t' + ' '.join(cmds))
        ret_code = subprocess.call(cmds, shell=False)
        if ret_code == 0:
            logger.info('Done. Return code: %d.\n\tlog file: %s' % (ret_code, project['logFile']))
        else:
            logger.error('Failed. Return code: %d.\n\tPlease check the log: %s' % (ret_code, 
                project['logFile']))

    def enable_iap(self, project):
        project_path = self._projects[0]['projectPath']
        # ProjectSettings.asset
        project_settings_path = path.join(project_path, 'ProjectSettings/ProjectSettings.asset')
        logger.info('Edit %s' % project_settings_path)
        with open(project_settings_path, 'r+') as project_settings:
            new_lines = []
            for line in project_settings:
                tmp = line.strip()
                if tmp.startswith('cloudProjectId'):
                    new_lines.append('  cloudProjectId: %s\n' % project['cloudProjectId'])
                elif tmp.startswith('projectName'):
                    new_lines.append('  projectName: %s\n' % project['projectName'])
                elif tmp.startswith('organizationId'):
                    new_lines.append('  organizationId: %s\n' % project['organizationId'])
                else:
                    new_lines.append(line)
            project_settings.seek(0, 0)
            project_settings.writelines(new_lines)

        # UnityConnectSettings.asset
        connect_settings_path = path.join(project_path,
                                          'ProjectSettings/UnityConnectSettings.asset')
        logger.info('Edit %s' % connect_settings_path)
        with open(connect_settings_path, 'r+') as connect_settings:
            new_lines = []
            found = False
            for line in connect_settings:
                tmp = line.strip()
                if found and tmp.startswith('m_Enabled'):
                    new_lines.append('    m_Enabled: 1\n')
                    continue
                if tmp.startswith('UnityPurchasingSettings') or \
                    tmp.startswith('UnityAnalyticsSettings'):
                    found = True
                    new_lines.append(line)
                else:
                    new_lines.append(line)
            connect_settings.seek(0, 0)
            connect_settings.writelines(new_lines)


def main():
    batchmode = BatchMode(path.abspath(path.join(path.dirname(__file__), './config.json')))
    batchmode.build()


if __name__ == '__main__':
    main()
