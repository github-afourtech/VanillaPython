__author__ = 'Mudit Srivastav'

from Generic.ReadConfig import Config
import subprocess
import fnmatch
import os
import sys

objConfig = Config()
objConfig.setConfigValues()
bFullSuiteExecution = objConfig.bFullSuite
sBatchExecutionFileName = objConfig.sBatchFileName
sOperatingSystem = objConfig.sOS
sProjectPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))

if sProjectPath.replace("\\", "\\\\") not in sys.path:
    sys.path.append(sProjectPath.replace("\\", "\\\\"))


def all_test_modules(root_dir, pattern):
    test_file_names = all_files_in(root_dir, pattern)
    return test_file_names


def check_if_testexist_infile(test_name):
    Flag = ""
    sBatchFilePath = os.path.join(sProjectPath, sBatchExecutionFileName)
    print sBatchFilePath

    with open(sBatchFilePath, 'r') as logfile:
        for line in logfile:
            # print("Lines from file",line)
            if line.strip() == test_name:
                Flag = True
                break
            else:
                Flag = False

    if Flag:
        return True
    else:
        return False


def all_files_in(root_dir, pattern):
    matches = []

    for root, dirnames, filenames in os.walk(root_dir):
        for filename in fnmatch.filter(filenames, pattern):

            if check_if_testexist_infile(filename):
                matches.append(filename)
                print(filename)

    return matches


def changeDirectory():
    if sOperatingSystem.lower() == "windows":
        process = subprocess.Popen("cd "+sProjectPath+"\TestScript", shell=True)
    else:
        process = subprocess.Popen("cd " + sProjectPath + "/TestScript", shell=True)
    process.wait()
    print process.returncode
    return process.returncode

def executeCommand():
    if bFullSuiteExecution==True:
        process = subprocess.Popen("py.test --alluredir "+sProjectPath+"\AllureReports", shell=True)
        process.wait()
        print process.returncode
        return process.returncode
    else:
        module_names = all_test_modules('.', 'test*.py')
        module_names = ' '.join(module_names)
        print(module_names)
        if sOperatingSystem.lower()=="windows":
            process = subprocess.Popen("cd "+sProjectPath+"/TestScript& py.test "+module_names+" --alluredir "+sProjectPath+"/AllureReports",shell=True)
        else:
            process = subprocess.Popen("cd "+sProjectPath+"/TestScript; py.test " + module_names + " --alluredir "+sProjectPath+"/AllureReports",shell=True)
        process.wait()
        print process.returncode
        return process.returncode


code = changeDirectory()
if code==0:
    code1 = executeCommand()
    print code1