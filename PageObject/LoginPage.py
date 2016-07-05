__author__ = 'Mudit Srivastav'

'''
Created on May 31, 2016
'''

from Generic.Wrappers import Wrappers
from selenium.webdriver.common.by import By


class LoginPageObjects():
    '''
    classdocs
    '''
    # This class contains all the methods to perform operations on login page.
    # All the required objects on the login page.

    txtBox_username = (By.ID, "username")
    txtBox_password = (By.ID, "password")
    btn_Login = (By.TAG_NAME,"button")
    btn_Logout = (By.XPATH, "//a[@href='/logout']")
    msg_Success_Error = (By.ID,"flash")

    def __init__(self, driver):
        # Create instance of Wrappers class
        self.objWrappers = Wrappers(driver)

    def enterLoginName(self, sLogin):
        self.objWrappers.enterText(self.txtBox_username, "Username", sLogin)

    def enterPassword(self, sPassword):
        self.objWrappers.enterText(self.txtBox_password, "Password", sPassword)

    def clickLogin(self):
        self.objWrappers.clickButton(self.btn_Login, "Login")

    def clickLogout(self):
        self.objWrappers.clickButton(self.btn_Logout, "Logout")

    def getLoginMessage(self):
        return self.objWrappers.getText(self.msg_Success_Error,"Message")

    # Regular login flow.
    def login(self, sLogin, sPassword):
        try:
            self.enterLoginName(sLogin)
            self.enterPassword(sPassword)
            self.clickLogin()

        except Exception as e:
            raise Exception("Error : {}".format(e))

    # Logout
    def logout(self):
        try:
            self.clickLogout()
        except Exception as e:
            raise Exception("Error : {}".format(e))

    # Success or Error Message
    def loginMessage(self):
        try:
            return (self.getLoginMessage()).decode('unicode_escape').encode('ascii', 'ignore').strip()
        except Exception as e:
            raise Exception("Error : {}".format(e))

    def getScreenshot(self,testMethodName):
        print self.objWrappers.get_base64_encoded_screen_shot(testMethodName+"_Assertion Error")
