#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os, errno
import threading
import yaml

from UniFileSync.lib.common.LogManager import logging

class ConfManager(object):
    """Configuration Manager for UniFileSync"""
    def __init__():
        ''' No __init__ is allowed '''
        pass

    __instance = None
    __lock     = threading.Lock()
    __confFile = None
    __confContent = None

    userHome   = os.path.expanduser('~')
    userPluginPath = '%s%s%s%s%s' % (userHome, os.sep, '.UniFileSync', os.sep, 'plugins')
    userConfPath = '%s%s%s%s%s' % (userHome, os.sep, '.UniFileSync', os.sep, 'conf')

    scriptHome = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    scriptPluginPath = '%s%s%s' % (scriptHome, os.sep, 'plugins')

    confPath   = '%s%s%s' % (scriptHome, os.sep, 'conf')
    confName   = 'UniFileSync.yaml'
    confFile   = confPath + os.sep + confName

    @staticmethod
    def getManager():
        """Get Plugin Manager instance"""
        ConfManager.__lock.acquire()
        if not ConfManager.__instance:
            ConfManager.__instance = super(ConfManager, ConfManager).__new__(ConfManager)
            super(ConfManager, ConfManager).__init__(ConfManager.__instance)
            ConfManager.__confFile = open(ConfManager.confFile, 'r')
            ConfManager.__confContent = ConfManager.__confFile.read()
            ConfManager.__instance.mkdir(ConfManager.userPluginPath)
            ConfManager.__instance.mkdir(ConfManager.userConfPath)
        ConfManager.__lock.release()
        return ConfManager.__instance

    def getValue(self, section, key):
        """get config value from key"""
        for content in yaml.load_all(self.__confContent):
            #print content
            if content['name'] == section:
                return content[key]

    def setValue(self, section, key, value):
        """set value to current key"""
        #print section, key, value, self.__confContent

        x = yaml.load_all(self.__confContent)

        for content in x:
            if content['name'] == section:
                content[key] = value
                print yaml.dump(content)

        for c in x:
            print c
        print yaml.dump_all(x)

    def getScriptHome(self):
        """get scrip path"""
        return ConfManager.scriptHome

    def getConfPaths(self):
        """get configuration path"""
        return [ConfManager.confPath, ConfManager.userConfPath]

    def getPluginPaths(self):
        """get plugin path"""
        return [ConfManager.scriptPluginPath, ConfManager.userPluginPath]

    def mkdir(self, path):
        """mkdir for UniFileSync self defined"""
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise

    def save(self):
        """save configuration into file"""
        self.__confFile.close()
        self.__confFile = open(self.confFile, 'w')
        self.__confFile.write(self.__confContent)
        self.__confFile.close()

    def __del__(self):
        """self-defined __del__function"""
        super(ConfManager, self).__del__()
        #self.save()

if __name__ == '__main__':
    print '%s' % ConfManager.getManager().getPluginPaths()
