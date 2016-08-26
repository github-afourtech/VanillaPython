from lxml import etree
from _elementtree import ParseError

'''
@author: AFour Technologies 
@param xmlFilePath: full path of xml file
@return: dict { UserGivenNameForElement:  {choosenIdentifier: locatorForElement} }
@note: This method reads xml and returns dict object.
'''


def readXML(xmlFilePath):
    try:
        doc = etree.parse(xmlFilePath) #If file is not found IO Exception is handled
        return {(Element.find('GivenName').text) : { Identifier.get('choosenIdentifier'): Identifier.text for Identifier in (Element.findall('Identifier')) } for Element in doc.getroot()}
        #If tag name is not found then AttributeError exception is handled                             
   
    except IOError as fileNotFound:
        print("xml file not found at given location" +xmlFilePath)
    
    except AttributeError as invalidUserGivenName:
        print("GivenName tag is not found in xml file")
        