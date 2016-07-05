__author__ = 'Mudit Srivastav'

'''
Created on May 31, 2016
'''

from Generic.ReadConfig import Config
from selenium import webdriver
import logging
from time import strftime
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.remote_connection import LOGGER

class Base():

    objDriver = None
    objConfig = Config()
    objConfig.setConfigValues()
    project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sTime = strftime("%Y-%m-%d_%H-%M-%S")
    LOGGER.setLevel(logging.WARNING)
    # Respective logging levels are set as defined in the Config file.
    Levels = {
        'debug' : logging.DEBUG,
        'info' : logging.INFO,
        'warning' : logging.WARNING,
        'error' : logging.ERROR,
        'critical' : logging.CRITICAL
    }

    # CRITICAL = 50
    # FATAL = CRITICAL
    # ERROR = 40
    # WARNING = 30
    # WARN = WARNING
    # INFO = 20
    # DEBUG = 10
    # NOTSET = 0

    level_name = objConfig.levelName
    level = Levels.get(level_name, logging.NOTSET)
    logger = logging.getLogger("execution_log")  #We can get the same logger instance throughout the project through this name
    LOG_FILENAME = os.path.join(project_path, 'Logs', "executionLog_" + sTime + '.log') #sets the name of log file
    hdlr = logging.FileHandler(os.path.join(project_path, 'Logs',  LOG_FILENAME))
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s') # sets the format of the logs printed in log file
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(level)

    def __init__(self):
        '''
        Constructor
        '''

    '''
    #    Function Name : OpenURL
    #    Description   : This function will get browser mentioned in config file and opens url in that browser
    #    Parameters    : None
    '''

    # Set up the driver according to the settings in configuration properties.
    # Open the application URL as specified in the Configuration settings if No url is passed while calling the method.
    def OpenURL(self, sURL=None):
        if Base.objConfig.sBrowserType == "Firefox":
            self.objDriver = webdriver.Firefox() # get instance of firefox driver
            self.logger.debug('Firefox instance started.')
        elif Base.objConfig.sBrowserType == "Ie":
            self.objDriver = webdriver.Ie(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), 'Driver',  'IEDriverServer.exe')) # get instance of IE driver
            self.logger.debug('IE instance started.')
        elif Base.objConfig.sBrowserType == "Chrome":
            capabilities = DesiredCapabilities.CHROME
            # get instance of Chrome driver
            self.objDriver = webdriver.Chrome(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), 'Driver', 'chromedriver.exe'),desired_capabilities=capabilities)
            self.logger.debug('Chrome instance started.')
        elif Base.objConfig.sBrowserType == "PhantomJS":
            # get instance of PhantomJS driver
            self.objDriver = webdriver.PhantomJS(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), 'Driver', 'phantomjs.exe'))
            self.logger.debug('PhantomJS instance started.')
        else:
            # get instance of chrome driver
            self.objDriver = webdriver.Ie(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), 'Driver', 'chromedriver.exe'))
            self.logger.debug('Chrome instance started.')

        # Set implicit wait value as defined in the Config file.
        if Base.objConfig.sTimeoutType == "Max":
            self.objDriver.implicitly_wait(long(Base.objConfig.lMaxTimeout))
        elif Base.objConfig.sTimeoutType == "Mid":
            self.objDriver.implicitly_wait(long(Base.objConfig.lMidTimeout))
        else:
            self.objDriver.implicitly_wait(long(Base.objConfig.lMinTimeout))

        if (sURL == None):
            self.objDriver.get(Base.objConfig.sURL)
        else:
            self.objDriver.get(sURL)

        self.objDriver.maximize_window() # Maximizes the window.

    '''
        # Get the prject path for the current project
    '''

    def get_project_path(self):
        """ Get the prject path for the current project"""
        try:
            project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            return project_path
        except Exception:
            raise Exception("Unable to get project path")