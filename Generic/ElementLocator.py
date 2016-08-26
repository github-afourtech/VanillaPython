from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By       
from Generic.Base import Base 
from selenium.common.exceptions import NoSuchElementException
import logging
        

def getLocatedElement(driver, dictElement, userGivenName):   
    '''
    @author: AFour Technologies
    @param driver: Web Driver object
    @param dictElement: all Locators and values in dict
    @param userGivenName: user given element name 
    @return: Finds working element from all listed values and if not found returns None
    @note: User can use multiple values with any Locator type and find working element by this method. This method is called from page object for finding working element. 
    '''
    workingElement = None 
    for Locator in dictElement.get(userGivenName).keys(): # Iterating over all Locators listed for single element by user in xml file.
        workingElement = getWorkingElement(driver, dictElement, userGivenName, Locator) # Finding element with associated locator:value. If element found returns element otherwise returns None in finally block after handling exception.    
        if(workingElement != None):
            return workingElement  #returns found element to associated page from where it is being called. 
        
    return workingElement     #return None  #End of for loop. No Element found defined with associated Exception
        
    
def getWorkingElement(driver, dictElement, userGivenName, Locator):
    '''
    @author: AFour Technologies
    @param driver: Web Driver object
    @param dictElement: all Locators and values in dict.
    @param userGivenName: user given element name. 
    @param Locator: Single locator for finding element 
    @return: Finds working element using mentioned locator and its associated value and if it is not found returns None 
    '''
    try:    
        workingElement = None
        # Following methods are forward declaration in order to locate element
        def findByXpath(value):
            return driver.find_element_by_xpath(value) #If Element is not found NoSuchElementException is defined
        
        def findById(value):
            return driver.find_element_by_id(value) #If Element is not found NoSuchElementException is defined
            
        def findByName(value):
            return driver.find_element_by_name(value)  #If Element is not found NoSuchElementException is defined
            
        def findByClassName(value):
            return driver.find_element_by_class_name(value)  #If Element is not found NoSuchElementException is defined
            
        def findByLinkText(value):
            return driver.find_element_by_link_text(value)  #If Element is not found NoSuchElementException is defined
            
        def findByPartialLinkText(value):
            return driver.find_element_by_partial_link_text(value)  #If Element is not found NoSuchElementException is defined
           
        def findByCssSelector(value):
            return driver.find_element_by_css_selector(value)  #If Element is not found NoSuchElementException is defined
            
        def findByTagName(value):
            return driver.find_element_by_tag_name(value)  #If Element is not found NoSuchElementException is defined
                
        # Following dict is forward declaration for switching methods, works equivalent to switch case in java.
        options = {"XPATH"               : findByXpath,
                       "ID"              : findById,
                       "NAME"            : findByName,
                       "CLASSNAME"       : findByClassName,
                       "LINKTEXT"        : findByLinkText,
                       "PARTIALLINKTEXT" : findByPartialLinkText,
                       "CSSSELECTOR"     : findByCssSelector,
                       "TAGNAME"         : findByTagName
                       }
        
        # Following line calls associated switch case by getting parameter as Locator type and its associated value
        workingElement = options[(Locator.upper())](dictElement.get(userGivenName).get(Locator)) 
        if workingElement.is_displayed():  # Checks weather element is displayed or not
            if workingElement.is_enabled(): # Checks weather element is enabled or not
                return workingElement       # Returns working element to getLocatedElement method
                        
    except NoSuchElementException as elementNotPreseent:  # Handling exception if element is not found
        print("Given Element not found on page" +elementNotPreseent.print_exc())
            
    finally:    # Returns None or working element in order to continue locating element by next Locator:Value pair 
        if(workingElement == None):
            return None
        if(workingElement != None):
            return workingElement    