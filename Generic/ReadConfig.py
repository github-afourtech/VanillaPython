__author__ = 'Mudit Srivastav'
'''
Created on May 31, 2016
'''

import ConfigParser
import os

class Config():
    sURL = ""
    sBrowserType = ""
    lMinTimeout = 0
    lMaxTimeout = 0
    lMidTimeout = 0
    sTimeoutType = ""
    sBatchFileName = ""
    bFullSuite = True
    sOS = ""
    levelName = "info"

    '''
    classdocs
    '''

    # Read the configuration properties and store them so they can be referred as required.
    def __init__(self):
        '''
        Constructor
        '''

    def setConfigValues(self):
        objConfig = ConfigParser.ConfigParser()

        objConfig.read(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),'config.Properties'))

        Config.sURL = objConfig.get("Application", "URL")
        Config.sBrowserType = objConfig.get("Environment", "BrowserType")
        Config.lMinTimeout = objConfig.get("Timeout", "MinTimeOut")
        Config.lMidTimeout = objConfig.get("Timeout", "MidTimeOut")
        Config.lMaxTimeout = objConfig.get("Timeout", "MaxTimeOut")
        Config.sTimeoutType = objConfig.get("Timeout", "TimeoutType")
        Config.sBatchFileName = objConfig.get("BatchFileName", "FileName")
        Config.bFullSuite = objConfig.get("Execution", "FullSuite")
        Config.sOS = objConfig.get("OperatingSystem","OS")
        Config.levelName = objConfig.get("LoggingLevel", "levelName")
