__author__ = 'Mudit Srivastav'
'''
Created on May 31, 2016
'''

from Generic.Base import Base
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import sys
import imaplib
import getpass
import email
import email.header
import datetime
import re
import os
import base64
import logging


class BasePage(object):
    def __init__(self, driver):
        # Create the wait object
        self.objDriver = driver
        self.objDriverWait = WebDriverWait(self.objDriver, long(Base.objConfig.lMidTimeout))


class Wrappers(BasePage):
    """

    """
    logger = logging.getLogger("execution_log")  # A logger instance is created in Base class with name "execution_log" to get the same instance of logger we have to write this line where we want to use log

    '''
       # Click the given button if it exists and is displayed on the page
    '''
    def clickButton(self, objObject, sObjName, iRowNo=0):
        """
        Click the given button if it exists and is displayed on the page
        :param objObject: element object
        :param sObjName: object Name
        :param iRowNo: row number
        :return:
        """
        try:
            if iRowNo == 0:
                if self.is_clickable(objObject, sObjName):
                    objElement = self.objDriverWait.until(EC.presence_of_all_elements_located(objObject))
                    objElement[0].click()
                    # print sObjName + " clicked successfully."
                    # self.logger.info(sObjName + " clicked successfully.")
                else:
                    print self.get_base64_encoded_screen_shot('clickButton')
                    print "Element " + sObjName + " not click-able."
                    self.logger.error("Element " + sObjName + " not click-able.")
                    raise Exception("Element " + sObjName + " not click-able.")
            else:
                if self.is_clickable(objObject, sObjName):
                    objElement = []
                    objElement = self.objDriver.find_elements(*objObject)
                    iRowNo = int(iRowNo)

                    objElement[iRowNo].click()
                    # print sObjName + " clicked successfully."
                    # self.logger.info(sObjName + " clicked successfully.")
                else:
                    print self.get_base64_encoded_screen_shot('clickButton')
                    print "Element " + sObjName + " not click-able."
                    self.logger.error("Element " + sObjName + " not click-able.")
                    raise Exception("Element " + sObjName + " not click-able.")
        except Exception as e:
            print self.get_base64_encoded_screen_shot('clickButton')
            print "ERROR: while finding the element " + sObjName, "Error: {}".format(e)
            self.logger.error("ERROR: while finding the element " + sObjName, "Error: {}".format(e))
            raise Exception("ERROR: while finding the element " + sObjName, "Error: {}".format(e))

    '''
    # Click the given link if it exists and is displayed on the page
    '''
    def clickLink(self, objObject, sObjName, iRowNo=0):
        """
        Click the given link if it exists and is displayed on the page
        :param objObject: element Object
        :param sObjName: object name
        :param iRowNo: row number
        :return:
        """
        try:
            objElement = self.objDriver.find_elements(*objObject)
            if self.is_clickable(objObject, sObjName):
                objElement[iRowNo].click()
                # print sObjName + " clicked successfully."
                # self.logger.info(sObjName + " clicked successfully.")
            else:
                print self.get_base64_encoded_screen_shot('clickLink')
                print "Element " + sObjName + " not click-able."
                self.logger.error("Element " + sObjName + " not click-able.")
                raise Exception("Element " + sObjName + " not click-able.")
        except Exception as e:
            print self.get_base64_encoded_screen_shot('clickLink')
            print "ERROR: while finding the element " + sObjName, "Error: {}".format(e)
            self.logger.error("ERROR: while clicking the element " + sObjName, "Error: {}".format(e))
            raise Exception("ERROR: while clicking the element " + sObjName, "Error: {}".format(e))

    '''
    # Enter the given text in the input box if it exists and is displayed on the page
    '''
    def enterText(self, objObject, sObjName, sText, iRowNo=0):
        """
        Enter the given text in the input box if it exists and is displayed on the page
        :param objObject: element Object
        :param sObjName: Object Name
        :param sText: text to be entered
        :param iRowNo: row number optional parameter
        :return:
        """
        try:
            if iRowNo == 0:
                objElement = self.objDriver.find_elements(*objObject)
                if self.is_visible(objObject, sObjName):
                    objElement[0].clear()
                    objElement[0].send_keys(sText)
                    # print "Value: " + sText + " entered for " + sObjName + " successfully."
                    # self.logger.info("Value: " + sText + " entered for " + sObjName + " successfully.")
                else:
                    print self.get_base64_encoded_screen_shot('enterText')
                    self.logger.error("Element " + sObjName + " not visible.")
                    raise Exception("Element " + sObjName + " not visible.")
            else:
                objElement = []
                objElement = self.objDriver.find_elements(*objObject)
                iRowNo = int(iRowNo)
                if self.is_visible(objObject, sObjName):
                    objElement[iRowNo - 1].clear()
                    objElement[iRowNo - 1].send_keys(sText)
                    # print "Value: " + sText + " entered for " + sObjName + " successfully."
                    # self.logger.info("Value: " + sText + " entered for " + sObjName + " successfully.")
                else:
                    print self.get_base64_encoded_screen_shot('enterText')
                    print "Element " + sObjName + " not visible."
                    self.logger.error("Element " + sObjName + " not visible.")
                    raise Exception("Element " + sObjName + " not visible.")
        except Exception as e:
            print self.get_base64_encoded_screen_shot('enterText')
            print "ERROR: while entering text in the element " + sObjName, "Error: {}".format(e)
            self.logger.error("ERROR: while entering text in the element " + sObjName, "Error: {}".format(e))
            raise Exception( "ERROR: while entering text in the element " + sObjName, "Error: {}".format(e))

    '''
    # Wait for the object to become visible. If it becomes visible in the given time, return true. Else return false.
    '''
    def is_visible(self, objObject, sObjName, iRowNo=0):
        """
        Wait for the object to become visible. If it becomes visible in the given time, return true. Else return false.
        :param objObject: element Object
        :param sObjName: Object Name
        :param iRowNo: Row number
        :return:
        """
        try:
            if iRowNo == 0:
                if self.objDriverWait.until(EC.visibility_of_element_located(objObject),
                                            'Timeout while checking the visibility of the element') is not None:
                    # print sObjName + " is visible."
                    # self.logger.info(sObjName + " is visible.")
                    return True
                else:
                    print "Element " + sObjName + " is not visible."
                    self.logger.error("Element " + sObjName + " not visible.")
                    print self.get_base64_encoded_screen_shot('is_visible')
                    return False
            else:
                objElement = []
                objElement = self.objDriver.find_elements(*objObject)
                iRowNo = int(iRowNo)
                if self.objDriverWait.until(EC.visibility_of(objElement[iRowNo - 1])) is not None:
                    # print sObjName + " is visible."
                    # self.logger.info(sObjName + " is visible.")
                    return True
                else:
                    print "Element " + sObjName + " is not visible."
                    self.logger.error("Element " + sObjName + " not visible.")
                    print self.get_base64_encoded_screen_shot('is_visible')
                    return False
        except Exception as e:
            print self.get_base64_encoded_screen_shot('is_visible')
            print "ERROR: while checking visibility of the element " + sObjName, "Error: {}".format(e)
            self.logger.error("ERROR: while checking visibility of the element " + sObjName, "Error: {}".format(e))
            raise Exception("ERROR: while checking visibility of the element " + sObjName, "Error: {}".format(e))

    '''
    # This function will return checkbox selected state
    '''
    def getCheckboxSelection(self, objObject, iRowNo=0):
        """
        This function will return checkbox selected state
        :param objObject: element Object
        :param iRowNo: row number
        :return:
        """
        try:
            objElement = self.objDriver.find_elements(*objObject)
            return objElement[iRowNo].is_selected()
        except Exception as e:
            print self.get_base64_encoded_screen_shot('getCheckboxSelection')
            print "ERROR: while checking checkbox selection", "Error: {}".format(e)
            self.logger.error("ERROR: while checking checkbox selection", "Error: {}".format(e))
            raise Exception("ERROR: while checking checkbox selection " , "Error: {}".format(e))

    '''
    # This function will click on checkbox in order to select or deselect
    '''
    def clickCheckBox(self, objObject, iRowNo=0):
        """
        This function will click on checkbox in order to select or deselect
        :param objObject: element Object
        :param iRowNo: row number
        :return:
        """
        try:
            objElement = self.objDriver.find_elements(*objObject)
            objElement[iRowNo].send_keys(Keys.SPACE)
            # self.logger.info("Checkbox clicked.")
        except Exception as e:
            print self.get_base64_encoded_screen_shot('clickCheckBox')
            print "ERROR: while clicking checkbox", "Error: {}".format(e)
            self.logger.error("ERROR: while clicking checkbox", "Error: {}".format(e))
            raise Exception("ERROR: while clicking checkbox", "Error: {}".format(e))

    '''
    # Wait for the object to get rendered. If it is rendered in the given time, return true. Else return false.
    '''
    def objectExists(self, objObject, sObjName):
        """
        Wait for the object to get rendered. If it is rendered in the given time, return true. Else return false.
        :param objObject: element Object
        :param sObjName: Object Name
        :return:
        """
        try:
            if self.objDriverWait.until(EC.presence_of_element_located(objObject)) is not None:
                # print sObjName + " exists on page"
                # self.logger.info(sObjName + " exists on page")
                return True
            else:
                print sObjName + " does not exist on page"
                self.logger.error(sObjName + " does not exist on page")
                print self.get_base64_encoded_screen_shot('objectExists')
                return False
        except Exception as e:
            print self.get_base64_encoded_screen_shot('objectExists')
            print "ERROR: while checking existence of the element " + sObjName, "Error: {}".format(e)
            self.logger.error("ERROR: while checking existence of the element " + sObjName, "Error: {}".format(e))
            raise Exception( "ERROR: while checking existence of the element " + sObjName, "Error: {}".format(e))


    '''
    # Wait for the object to be rendered and become clickable. If it becomes clickable in the given time, return true. Else return false.
    '''
    def is_clickable(self, objObject, sObjName):
        """
        Wait for the object to be rendered and become clickable. If it becomes clickable in the given time, return true. Else return false.
        :param objObject: element Object
        :param sObjName: object Name
        :return:
        """
        try:
            if self.is_visible(objObject, sObjName):
                if self.objDriverWait.until(EC.element_to_be_clickable(objObject), 'Timeout Exception') is not None:
                    # print sObjName + " is click-able."
                    # self.logger.info(sObjName + " is click-able.")
                    return True
                else:
                    print sObjName + " is not click-able."
                    self.logger.error(sObjName + " is not click-able.")
                    print self.get_base64_encoded_screen_shot('is_clickable')
                    return False
            else:
                self.logger.error(sObjName + " is not visible.")
                return False
        except Exception as e:
            print self.get_base64_encoded_screen_shot('is_clickable')
            print "ERROR: while checking click-ability of the element " + sObjName + " Error: {}".format(e)
            self.logger.error("ERROR: while checking click-ability of the element " + sObjName + " Error: {}".format(e))
            raise Exception("ERROR: while checking click-ability of the element " + sObjName + " Error: {}".format(e))

    '''
    # Check if the given object is enabled
    '''
    def isEnabled(self, objObject, sObjName, iRowNo=0):
        """
        Check if the given object is enabled
        :param objObject: element Object
        :param sObjName: Object Name
        :param iRowNo: row number
        :return:
        """
        try:
            if self.objectExists(objObject, sObjName):
                objElement = self.objDriver.find_elements(*objObject)
                return objElement[iRowNo].is_enabled()
            else:
                self.logger.error(sObjName + " is not enabled.")
                return False
        except Exception as e:
            print self.get_base64_encoded_screen_shot('isEnabled')
            self.logger.error("ERROR: while checking if the element " + sObjName + " is enabled. Error: {}".format(e))
            raise Exception("ERROR: while checking if the element " + sObjName + " is enabled. Error: {}".format(e))

    '''
    # Check if the given string exists on the entire page. Return true if found.
    # If object is provided, wait till the object is visible and then check for the string in the page source.
    '''
    def textExistsOnPage(self, sString, objObject=None, sObjName=""):
        """
        Check if the given string exists on the entire page. Return true if found.
        If object is provided, wait till the object is visible and then check for the string in the page source.
        :param sString: String to be verified
        :param objObject: element Object
        :param sObjName: object Name
        :return:
        """
        try:
            if objObject is not None:
                if self.is_visible(objObject, sObjName):
                    return sString in self.objDriver.page_source
            else:
                return sString in self.objDriver.page_source
        except Exception as e:
            print self.get_base64_encoded_screen_shot('textExistsOnPage')
            print "ERROR: while checkiing text exists on page. Error: {}".format(e)
            self.logger.error("ERROR: while checkiing text exists on page. Error: {}".format(e))
            raise Exception("ERROR: while checking text exists on page. Error: {}".format(e))

    '''
    # Check if the given string exists in the text of the given control. Check if the control is present on the page, get it's text
    # and then check if the text contains the given string. Return true if found.
    '''
    def textExistsInControl(self, objObject, sObjName, sString, iRowNo=0):
        """
        Check if the given string exists in the text of the given control. Check if the control is present on the page, get it's text
        and then check if the text contains the given string. Return true if found.
        :param objObject: String to be verified
        :param sObjName: Object Name
        :param sString: String to be verified
        :param iRowNo: row number
        :return:
        """
        try:
            if iRowNo == 0:
                if self.is_visible(objObject, sObjName):
                    if self.objDriverWait.until(EC.text_to_be_present_in_element((objObject), sString)):
                        objElement = self.objDriver.find_element(*objObject)
                        if objElement is not None:
                            # print sString + " found in " + sObjName
                            # self.logger.info(sString + " found in " + sObjName)
                            return sString.lower() in objElement.text.lower()
                        else:
                            print sString + " not found in " + sObjName
                            self.logger.error(sString + " not found in " + sObjName)
                            return False
                    else:
                        print sString + " "
                        return False
            else:
                objElement = []
                objElement = self.objDriver.find_elements(*objObject)
                iRowNo = int(iRowNo)
                return sString.lower() in objElement[iRowNo].text.lower()
        except Exception as e:
            print self.get_base64_encoded_screen_shot('textExistsInControl')
            print "ERROR: while checking if text '" + sString + "' exists in element " + sObjName + " Error: {}".format(e)
            self.logger.error("ERROR: while checking if text '" + sString + "' exists in element " + sObjName + " Error: {}".format(e))
            raise Exception("ERROR: while checking if text '" + sString + "' exists in element " + sObjName + " Error: {}".format(e))

    '''
    # Return the text of the control if it exists.
    # objObject is the sequence, not the webelement
    '''
    def getText(self, objObject, sObjName, iRowNo=0):
        """
        Return the text of the control if it exists.
        objObject is the sequence, not the webelement
        :param objObject: element Object
        :param sObjName: Object Name
        :param iRowNo: row number
        :return:
        """
        try:
            if iRowNo == 0:
                if self.objectExists(objObject, sObjName):
                    objElement = self.objDriver.find_elements(*objObject)
                    return objElement[0].text.encode("utf-8")
                else:
                    print self.get_base64_encoded_screen_shot('getText')
                    self.logger.error(sObjName + " not found on the page.")
                    raise Exception(sObjName + " not found on the page.")
            else:
                objElement = []
                objElement = self.objDriver.find_elements(*objObject)

                iRowNo = int(iRowNo)
                return objElement[iRowNo].text
        except Exception as e:
            print self.get_base64_encoded_screen_shot('getText')
            print "ERROR: while getting text of element " + sObjName + " Error: {}".format(e)
            self.logger.error("ERROR: while getting text of element " + sObjName + " Error: {}".format(e))
            raise Exception("ERROR: while getting text of element " + sObjName + " Error: {}".format(e))

    '''
    # Return the text of the control if it exists.
    # objObject is the webelement
    '''
    def getTextForWebElement(self, objObject, sObjName):
        """
        Return the text of the control if it exists.
        objObject is the webelement
        :param objObject: element Object
        :param sObjName: object name
        :return:
        """
        try:
            # objElement = self.objDriver.find_element(objObject)
            return objObject.text
        except Exception as e:
            print self.get_base64_encoded_screen_shot('getTextForWebElement')
            print "ERROR: while getting text of element " + sObjName + " Error: {}".format(e)
            self.logger.error("ERROR: while getting text of element " + sObjName + " Error: {}".format(e))
            raise Exception("ERROR: while getting text of element " + sObjName + " Error: {}".format(e))

    '''
    # Return the value of the control if it exists.
    # objObject is the sequence, not the webelement
    '''
    def getValue(self, objObject, sObjName, iRowNo=0):
        """
        Return the value of the control if it exists.
        objObject is the sequence, not the webelement
        :param objObject: element Object
        :param sObjName: object Name
        :param iRowNo: row number
        :return:
        """
        try:
            if self.objectExists(objObject, sObjName):
                objElement = self.objDriver.find_elements(*objObject)
                return objElement[iRowNo].get_attribute("value")
            else:
                self.logger.error(sObjName + " not found on the page.")
                raise Exception(sObjName + " not found on the page.")
        except Exception as e:
            print self.get_base64_encoded_screen_shot('getValue')
            print "ERROR: while getting value of element " + sObjName + " Error: {}".format(e)
            self.logger.error("ERROR: while getting value of element " + sObjName + " Error: {}".format(e))
            raise Exception("ERROR: while getting value of element " + sObjName + " Error: {}".format(e))

    '''
    # Returns object attribute specified as a parameter
    # objObject is the sequence, not the webelement
    '''
    def getAttribute(self, objObject, sObjName, sAttribute):
        """
        Returns object attribute specified as a parameter
        objObject is the sequence, not the webelement
        :param objObject: element Object
        :param sObjName: object Name
        :param sAttribute: attribute name
        :return:
        """
        try:
            if self.objectExists(objObject, sObjName):
                objElement = self.objDriver.find_element(*objObject)

                return objElement.get_attribute(sAttribute)
            else:
                raise Exception(sObjName + " not found on the page.")
        except Exception as e:
            print self.get_base64_encoded_screen_shot('getAttribute')
            print "ERROR: while getting attribute of element " + sObjName + " Error: {}".format(e)
            self.logger.error("ERROR: while getting attribute of element " + sObjName + " Error: {}".format(e))
            raise Exception("ERROR: while getting attribute of element " + sObjName + " Error: {}".format(e))

    '''
    # Return the value of the given attribute for the element. The element is passed as webelement
    # and not as the sequence.
    '''
    def getAttributeForWebElement(self, objObject, sObjName, sAttribute):
        """
        Return the value of the given attribute for the element. The element is passed as webelement
        and not as the sequence.
        :param objObject: element Object
        :param sObjName: Object name
        :param sAttribute: attribute name
        :return:
        """
        try:
            return objObject.get_attribute(sAttribute)
        except Exception as e:
            print self.get_base64_encoded_screen_shot('getAttributeForWebElement')
            print "ERROR: while getting attribute of element " + sObjName + " Error: {}".format(e)
            self.logger.error("ERROR: while getting attribute of element " + sObjName + " Error: {}".format(e))
            raise Exception("ERROR: while getting attribute of element " + sObjName + " Error: {}".format(e))

    '''
    #  Set the value of the radio button
    '''
    def setRadioButtonByValue(self, objObject, sObjName, sValue):
        """
        Set the value of the radio button
        :param objObject: element Object
        :param sObjName: object Name
        :param sValue: Radio button value
        :return:
        """
        try:
            if self.objectExists(objObject, sObjName):
                objElement = self.objDriver.find_elements(*objObject)
                for element in objElement:
                    if element.get_attribute("value") == sValue:
                        element.click()
                        break;
                else:
                    self.logger.error(sValue + " not found in the dropdown " + sObjName)
                    raise Exception(sValue + " not found in the dropdown " + sObjName)
            else:
                self.logger.error(sObjName + " not found on the page.")
                raise Exception(sObjName + " not found on the page.")
        except Exception as e:
            print self.get_base64_encoded_screen_shot('setRadioButtonByValue')
            print "ERROR: while setting radio button value of element " + sObjName + " Error: {}".format(e)
            self.logger.error("ERROR: while setting radio button value of element " + sObjName + " Error: {}".format(e))
            raise Exception("ERROR: while setting radio button value of element " + sObjName + " Error: {}".format(e))

    '''
    # Return all the elements of the given type in the given container/parent.
    # e.g. all links in a section or buttons in a div, etc.
    '''
    def elementsInContainer(self, objObject, sType):
        """
        Return all the elements of the given type in the given container/parent.
        e.g. all links in a section or buttons in a div, etc.
        :param objObject:
        :param sType:
        :return:
        """
        try:
            objElements = []
            objContainer = self.objDriver.find_element(*objObject)
            objElements = objContainer.find_elements(*sType)
            return objElements
        except Exception as exp:
            raise  Exception("Error : {}".format(exp))

    '''
    #  Return all the child elements of the given tag for the given parent element
    # The parent element is passed as webelement rather than the sequence
    '''

    def getChildElementsByTag(self, objParent, sTag):
        """
        @param objParent:
        @param sTag:
        @return:
        """
        try:
            objChild = []
            objChild = objParent.find_elements(*sTag)

            return objChild
        except Exception as exp:
            raise Exception("ERROR: while getting children elements of type " + sTag + " . " + "Error: {}".format(exp))


    '''
    # An Expectation for checking that an element is either invisible or not present on the DOM.
    '''
    def isNotVisible(self, objObject, sObjName):
        """
        An Expectation for checking that an element is either invisible or not present on the DOM.
        :param objObject:
        :param sObjName:
        :return:
        """
        try:
            if self.objDriverWait.until(EC.invisibility_of_element_located(objObject),
                                        'TimeOut while checking the invisibility of the element') is not None:
                # print sObjName + " is not visible."
                # self.logger.info(sObjName + " is not visible.")
                return True
            else:
                print sObjName + " is visible."
                self.logger.error(sObjName + " is visible.")
                return False
        except Exception as e:
            print self.get_base64_encoded_screen_shot('isNotVisible')
            print "ERROR: while checking invisibility of the element " + "{}".format(e)
            self.logger.error("ERROR: while checking invisibility of the element " + "{}".format(e))
            raise Exception("ERROR: while checking invisibility of the element " + "{}".format(e))


    '''
    # Select the given value from the dropdown
    '''
    def selectValueFromDropdown(self, objObject, sObjName, sValue):
        """
        Select the given value from the dropdown
        :param objObject:
        :param sObjName:
        :param sValue:
        :return:
        """
        try:
            cboSelect = Select(self.objDriver.find_element(*objObject))
            cboSelect.select_by_visible_text(sValue)
        except Exception as e:
            print self.get_base64_encoded_screen_shot('selectValueFromDropdown')
            print "ERROR: while selecting value from dropdown: " + "Error : {}".format(e)
            self.logger.error("ERROR: while selecting value from dropdown: " + "Error : {}".format(e))
            raise Exception("ERROR: while selecting value from dropdown: " + "Error : {}".format(e))

    '''
    # Switch to the given iFrame
    '''
    def switchToFrame(self, objObject, sObjName):
        """
        Switch to the given iFrame
        :param objObject:
        :param sObjName:
        :return:
        """
        try:
            objFrame = self.objDriver.find_element(*objObject)
            self.objDriver.switch_to_frame(objFrame)
            # print "Switched successfully to frame: " + sObjName
            # self.logger.info("Switched successfully to frame: " + sObjName)
        except Exception as e:
            print self.get_base64_encoded_screen_shot('switchToFrame')
            self.logger.error("ERROR: while switching to iFrame: " + "Error: {}".format(e))
            raise Exception("ERROR: while switching to iFrame: " + "Error: {}".format(e))

    '''
    # Switch back from the iFrame to default content
    '''
    def switchToDefault(self):
        """
        Switch back from the iFrame to default content
        :return:
        """
        try:
            self.objDriver.switch_to_default_content()
        except Exception as e:
            raise Exception("ERROR: while switching to Default: " + "Error: {}".format(e))

    '''
    # This function will refresh Page
    '''
    def refreshPage(self):
        """
        This function will refresh Page
        :return:
        """
        try:
            self.objDriver.refresh()
        except Exception as e:
            raise Exception("Error: while refreshing page: {} Error : {}".format(e))

    '''
    #    This function will return array of elements of same type
    '''
    def getElements(self, objObject):
        """
        This function will return array of elements of same type
        :param objObject:
        :return:
        """
        try:
            objElements = []
            objElements = self.objDriver.find_elements(*objObject)
            return objElements
        except Exception as exp:
            raise Exception("Error : {}".format(exp))

    '''
    #    This function will drag and drop an element from source location to target location
    '''

    def dragAndDrop(self, sourceElement, destElement, sObjSourceName, sObjDestinationName):
        """
        This function will drag and drop an element from source location to target location
        :param sourceElement:
        :param destElement:
        :param sObjSourceName:
        :param sObjDestinationName:
        :return:
        """
        try:
            if self.objectExists(sourceElement, sObjSourceName):
                if self.objectExists(destElement, sObjDestinationName):
                    source = self.objDriver.find_element(*sourceElement)
                    destination = self.objDriver.find_element(*destElement)
                    ActionChains(self.objDriver).drag_and_drop(source, destination).perform()
        except Exception as exp:
            print self.get_base64_encoded_screen_shot('dragAndDrop')
            self.logger.error("Error: while drag and drop: {} Error : {}".format(exp))
            raise Exception("Error: while drag and drop: {} Error : {}".format(exp))

    '''
    # This function will mousehover and click on the given element
    '''
    def mouseHoverAndClick(self, objToMouseOver, objToClick, sObjName, iRowNo=0):
        """
        This function will mouseover and click on the given element
        :param objToMouseOver:
        :param objToClick:
        :param sObjName:
        :param iRowNo:
        :return:
        """
        try:
            objElement = self.objDriverWait.until(EC.visibility_of_element_located(objToMouseOver))
            hov1 = ActionChains(self.objDriver).move_to_element(objElement)
            hov1.perform()
            objClick = self.objDriverWait.until(EC.presence_of_all_elements_located(objToClick))
            hov2 = ActionChains(self.objDriver).move_to_element(objClick[iRowNo])
            hov3 = ActionChains(self.objDriver).double_click(objClick[iRowNo])
            hov2.perform()
            hov3.perform()
        except Exception as exp:
            print self.get_base64_encoded_screen_shot('mouseOverAndClick')
            self.logger.error("Error: while doing mouseOverAndClick: {} Error : {}".format(exp))
            raise Exception("Error: while doing mouseOverAndClick: {} Error : {}".format(exp))

    '''
    #  Hover the mouse over the given object. Typically used where there's a menu dropdown to be accessed
    # which opens up after mouse hover.
    '''
    def mouseHover(self, objObject, sObjName):
        """
         Hover the mouse over the given object. Typically used where there's a menu dropdown to be accessed
         which opens up after mouse hover.
        :param objObject:
        :param sObjName:
        :return:
        """
        try:
            objElement = self.objDriverWait.until(EC.visibility_of_element_located(objObject))
            actHover = ActionChains(self.objDriver).move_to_element(objElement)
            actHover.perform()
        except Exception as e:
            print self.get_base64_encoded_screen_shot('mouseHover')
            self.logger.error("Error: while doing mouseHover: {} Error : {}".format(e))
            raise Exception("Error: while doing mouseHover: {} Error : {}".format(e))

    '''
    # Move back or forward in the browser's history.
    '''
    def moveBrowserHistory(self, sDirection):
        """
        Move back or forward in the browser's history.
        :param sDirection:
        :return:
        """
        try:
            if (sDirection.lower() == "back"):
                self.objDriver.back()
            else:
                self.objDriver.forward()
        except Exception as e:
            print self.get_base64_encoded_screen_shot('moveBrowserHistory')
            self.logger.error("Error: while moving forward or backward: {} Error : {}".format(e))
            raise Exception("Error: while moving forward or backward: {} Error : {}".format(e))

    '''
    # Close any browser alert that is displayed. It may not be possible to check the text that is displayed in the alert
    # We are just pressing the Ok button and closing the alert. We are only checking that alert was displayed.
    '''
    def closeBrowserAlert(self):
        """
        Close any browser alert that is displayed. It may not be possible to check the text that is displayed in the alert
        We are just pressing the Ok button and closing the alert. We are only checking that alert was displayed.
        :return:
        """
        try:
            alert = self.objDriver.switch_to_alert()
            alert.accept()
        except Exception as e:
            print self.get_base64_encoded_screen_shot('closeBrowserAlert')
            print "Error: while closing alert: {} Error : {}".format(e)
            self.logger.error("Error: while closing alert: {} Error : {}".format(e))
            raise Exception("Error: while closing alert: {} Error : {}".format(e))

    '''
    # Get the URL of the current page
    '''
    def getCurrentURL(self):
        """
        Get the URL of the current page
        :return:
        """
        return self.objDriver.current_url


    objServer = None

    '''
    # Connect to the gmail server using given login/password and select the specified folder.
    '''
    def connectToMailServer(self, sEmail, sPassword, sFolder):
        """
        Connect to the gmail server using given login/password and select the specified folder.
        :param sEmail:
        :param sPassword:
        :param sFolder:
        :return:
        """
        try:
            self.objServer = imaplib.IMAP4_SSL('imap.gmail.com')
            sReturn, objEmails = self.objServer.login(sEmail, sPassword)
            if sReturn == 'OK':
                print "Successfully connected to gmail server"
                sReturn, mailBoxes = self.objServer.list()
                if sReturn == 'OK':
                    print "Found folder " + sFolder + " in mailbox."
                    sReturn, objMailBox = self.objServer.select(sFolder)

        except Exception as e:
            raise Exception("ERROR: Error connecting to mail server. " + "Error: {}".format(e))

    '''
    # Find the first unread mail in the email folder for the given subject.
    # IMPORTANT: It is assumed that the mailbox is sorted on unread mails. If there are multiple emails found for the given filter,
    # it'll take the first one found.
    '''
    def findEmailBySubject(self, sSubject):
        """
        Find the first unread mail in the email folder for the given subject.
        IMPORTANT: It is assumed that the mailbox is sorted on unread mails. If there are multiple emails found for the given filter,
        it'll take the first one found.
        :param sSubject:
        :return:
        """
        try:
            sReturn, data = self.objServer.search(None, '(UNSEEN SUBJECT "%s")' % sSubject)
            if sReturn != 'OK':
                return 'No message found'
            else:
                sReturn = ""
                sMsg = ""
                for num in data[0].split():
                    sReturn, data = self.objServer.fetch(num, '(RFC822)')
                    sMsg = email.message_from_string(data[0][1])
                    print "Email message with subject: " + sSubject + " found."

                if (sMsg == ""):
                    print "Email message with subject: " + sSubject + " not found."
                    #             print sMsg
            return sMsg
        except Exception as e:
            raise Exception("ERROR: Error finding specified email in the mailbox. ", "Error: {}".format(e))

    '''
    # Get contents of the email as string. Currently, html emails are considered. Conditions for other content type to be added as required.
    '''
    def getEmailContent(self, sMsg):
        """
        Get contents of the email as string. Currently, html emails are considered. Conditions for other content type to be added as required.
        :param sMsg:
        :return:
        """
        try:
            sReturn = ""
            if sMsg is not None:
                if sMsg.is_multipart():
                    for sPart in sMsg.walk():
                        if sPart.get_content_type() == 'text/html':
                            sReturn = unicode(sPart.get_payload(decode=True), str(sPart.get_content_charset()),
                                              "ignore").encode('utf8', 'replace')
                            print "Contents of the email parsed successfully."
                            break
            else:
                print "Message could not be extracted from the email"
            return sReturn
        except Exception as e:
            raise Exception("ERROR: Error getting email contents. ", "Error: {}".format(e))


    '''
    # Extract the URL from the email. It'll return the first <a> tag found in the contents of the email so be careful if there are
    # multiple <a> tags in the email message.
    # This method can be directly called as it'll connect to the server, find the required email, extract the contents and return the URL.
    '''
    def getURLFromEmail(self, sEmail, sPassword, sFolder, sCondType, sSearchCond, sLink):
        """
        Extract the URL from the email. It'll return the first <a> tag found in the contents of the email so be careful if there are
        multiple <a> tags in the email message.
        This method can be directly called as it'll connect to the server, find the required email, extract the contents and return the URL.
        :param sEmail:
        :param sPassword:
        :param sFolder:
        :param sCondType:
        :param sSearchCond:
        :param sLink:
        :return:
        """
        try:
            self.connectToMailServer(sEmail, sPassword, sFolder)
            if sCondType.upper() == 'SUBJECT':
                sMsg = self.findEmailBySubject(sSearchCond)
            if (sMsg <> ""):
                sContent = self.getEmailContent(sMsg)
                print sContent
                if sContent != "":
                    print "href=(.+?)" + sLink

                    sReturn = re.search("href=(.+?)" + sLink, sContent)
                    print sReturn

                    if sReturn is not None:
                        return sReturn.group(1).replace('"', "").replace("'", "")
                    else:
                        print "Link cannot be extracted from the email message."
                        return "Not found"
                else:
                    print "Email contents could not be extracted."
                    return "Not found"
            else:
                print "No email message found for the given search criteria"
                return ""
        except Exception as e:
            raise Exception("ERROR: Error extracting URL from email content. ", "Error: {}".format(e))

    '''
    # Method to capture screenshot
    '''
    def get_base64_encoded_screen_shot(self, file_name):
        """
        Method to capture screenshot
        :param file_name:
        :return:
        """
        base = Base()
        abs_file_path = os.path.join(base.get_project_path(), 'ScreenShots',  file_name + '.png')
        self.objDriver.get_screenshot_as_file(abs_file_path)
        with open(abs_file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        img_element = 'b64EncodedStart{0}b64EncodedEnd'.format(encoded_string)
        return img_element