__author__ = 'Mudit Srivastav'
'''
Created on May 31, 2016
'''

from Generic.ReadConfig import Config
import fnmatch
import os
import unittest
import HTMLTestRunner
import sys
from time import strftime

objConfig = Config()
objConfig.setConfigValues()
sBatchExecutionFileName = objConfig.sBatchFileName
sProjectPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))

if sProjectPath.replace("\\", "\\\\") not in sys.path:
    sys.path.append(sProjectPath.replace("\\", "\\\\"))


def all_test_modules(root_dir, pattern):
    test_file_names = all_files_in(root_dir, pattern)
    return [path_to_module(str) for str in test_file_names]


def check_if_testexist_infile(test_name):
    Flag = ""
    # sBatchFilePath = sProjectPath + "/Vanilla_Python_BatchFile.txt"
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
                matches.append(os.path.join(root, filename))
                print(filename)

    return matches


def path_to_module(py_file):
    return strip_leading_dots( \
        replace_slash_by_dot( \
            strip_extension(py_file)))


def strip_extension(py_file):
    return py_file[0:len(py_file) - len('.py')]


def replace_slash_by_dot(str):
    return str.replace('\\', '.').replace('/', '.')


def strip_leading_dots(str):
    while str.startswith('.'):
        str = str[1:len(str)]
    return str


module_names = all_test_modules('.', 'test*.py')
print(module_names)
suites = [unittest.defaultTestLoader.loadTestsFromName(mname) for mname
          in module_names]

testSuite = unittest.TestSuite(suites)
runner = unittest.TextTestRunner(verbosity=1)
sTime = strftime("%Y-%m-%d_%H-%M-%S")
filename = sProjectPath + '/HTMLReports/Execution_Report_' + sTime + '.html'
output = open(filename, "wb")
sImagePath = sProjectPath + "/python.png"
output = open(filename, "wb")
runner = HTMLTestRunner.HTMLTestRunner(imgpath=sImagePath, stream=output, title="Vanilla Report")
runner.run(testSuite)