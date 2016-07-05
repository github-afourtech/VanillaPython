__author__ = 'Mudit Srivastav'
'''
Created on May 31, 2016
'''

import unittest
import allure
from ddt import ddt, data, unpack,file_data
from Generic.CSVDriver import get_csv_data
from Generic.Base import Base
from Generic.SkipIfTrue import skipIfTrue
from PageObject.LoginPage import LoginPageObjects
import logging
import os
from allure.constants import AttachmentType


'''
# DDT consists of a class decorator ddt (for your TestCase subclass) and two method decorators (for your tests that want to be multiplied):
# data: contains as many arguments as values you want to feed to the test.
# file_data: will load test data from a JSON file.
# Normally each value within data will be passed as a single argument to your test method. If these values are e.g. tuples, you will have to unpack them inside your test. Alternatively, you can use an additional decorator, unpack, that
# will automatically unpack tuples and lists into multiple arguments, and dictionaries into multiple keyword arguments.
'''
@ddt
class LoginPageMultipleTest(unittest.TestCase,Base):
    """ Inheriting the TestCase class."""

    bTest1 = False
    logger = logging.getLogger("execution_log")  # A logger instance is created in Base class with name "execution_log" to get the same instance of logger we have to write this line where we want to use log


    @allure.step('Test Login using Json') #By default step name is generated from method name for more info visit https://github.com/allure-framework/allure-python
    @file_data(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), 'TestData','login_test_Skip' + '.json')) # @file_data : will load test data from a JSON file.
    def test_1(self, data_set):
        """Test case for json test_1."""
        try:
            self.OpenURL(data_set['target_url'])
            self.objLogin = LoginPageObjects(self.objDriver)
            self.objLogin.login(data_set['username'], data_set['password'])
            print "Login Successful"  # Print message log is used for showing logs in Allure
            self.logger.info("Login Successfull") # This line is used to store log in log file generated in Logs folder.
            self.assertEqual(self.objLogin.loginMessage(), data_set['expectedMessage'])
            print "Message verification Successfull." # Print message log is used for showing logs in Allure
            self.logger.info("Message verification Successfull") # This line is used to store log in log file generated in Logs folder.
            self.objLogin.logout()
            print "Logout Successfull"  # Print message log is used for showing logs in Allure
            self.logger.info("Logout Successfull") # This line is used to store log in log file generated in Logs folder.
        except Exception as e:
            # self.objLogin.getScreenshot("test_1") # Use this line when you want to generate HTML Reports
            self.logger.error("{}".format(e)) # This line is used to store error logs in log file generated in Logs folder.
            allure.attach('screenshot', self.objDriver.get_screenshot_as_png(), type=AttachmentType.PNG) # Use this line when you want to generate Allure Reports
            LoginPageMultipleTest.bTest1 = True
            raise Exception("Error: {}".format(e))
        finally:
            self.objDriver.quit()



    @allure.step('Test Login')
    @data(*get_csv_data(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), 'TestData','login_csv_test_Skip' + '.csv'))) #data: contains as many arguments as values you want to feed to the test and get_csv_data is a method defined in CSVDriver class which returns rows of csv data file as a list.
    @unpack # This decoartor is used to unpack a row data and the value to the respective parameters of test_2 method.
    @skipIfTrue('bTest1') #@skipIfTrue(booleanVariableName), this tag will make test_2 to be skipped if Boolean variable bTest1 is True. Boolean variable bTest1 value is set in the dependent Test Method test_1.
    def test_2(self, target_url, username, password, expectedMessage):
        """Test case for test_2."""
        try:
            self.OpenURL(target_url)
            self.objLogin = LoginPageObjects(self.objDriver)
            self.objLogin.login(username, password)
            print "Login Successful"  # Print message log is used for showing logs in Allure
            self.logger.info("Login Successfull")  # This line is used to store log in log file generated in Logs folder.
            self.assertEqual(self.objLogin.loginMessage(), expectedMessage)
            print "Message verification Successfull"  # Print message log is used for showing logs in Allure
            self.logger.info("Message verification Successfull") # This line is used to store log in log file generated in Logs folder.
            self.objLogin.logout()
            print "Logout Successfull"  # Print message log is used for showing logs in Allure
            self.logger.info("Logout Successfull")  # This line is used to store log in log file generated in Logs folder.
        except Exception as e:  # Use this exception block when you want to generate Allure Reports
            # self.objLogin.getScreenshot("test_2")  # Use this line when you want to generate HTML Reports
            self.logger.error("{}".format(e))  # This line is used to store error logs in log file generated in Logs folder.
            allure.attach('screenshot', self.objDriver.get_screenshot_as_png(), type=AttachmentType.PNG) # Use this line when you want to generate Allure Reports
            raise Exception("Error: {}".format(e))
        finally:
            self.objDriver.quit()

if __name__ == '__main__':
    '''
    # Every module has a name and statements in a module can find out the name of its module. This is especially handy in one particular situation - As mentioned previously,
    # when a module is imported for the first time, the main block in that module is run. What if we want to run the block only if the program was used by itself and not when it was imported from another module? This can be achieved using the __name__ attribute of the module.
    # Every Python module has it's __name__ defined and if this is '__main__', it implies that the module is being run standalone by the user and we can do corresponding appropriate actions.
    '''
    unittest.main()
