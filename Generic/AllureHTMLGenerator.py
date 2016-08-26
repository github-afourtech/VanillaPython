from Generic.ReadConfig import Config
import subprocess
import os
import sys
import time

def allureHTMLGenerator():
    '''
    @author: AFour Technologies
    @param param: None
    @return: None
    @note: This function generates and opens AllueHTML report generated from AllureXML report
    '''
    objConfig = Config()
    objConfig.setConfigValues()
    sOperatingSystem = objConfig.sOS
    
    xmlFilesPath = (os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), 'AllureReports'))
    HTMLFilesPath = (os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), 'AllureHTMLReport'))
    
    
    if sOperatingSystem.lower()=="windows":  # Generating AlureHTML report is OS dependent  
        command = "allure generate " +xmlFilesPath +" -o " +HTMLFilesPath   # Command for generate AllureHTML report
        result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        time.sleep(7) # Need this time to generate HTML report
        command = "allure report open -o " +HTMLFilesPath  # Command for opening AllureHTML report 
        subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = result.communicate()
        if output:   # If report gets generated and opened successfully then return code(0) and output is printed on console since we can not log it in reporting. 
            print "return code: " ,result.returncode
            print "OK: output: " ,output
        if error:    # If report failed to generate Or open successfully then return code(1) and error is printed on console since we can not log it in reporting.
            print "return code: " ,result.returncode  
            print "Error: output: " ,error 
            print "Please download allure-cli from http://wiki.qatools.ru/display/AL/Allure+Commandline and mention .bat file path in system/user Path variable"    