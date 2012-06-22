'''
Created on Jun 21, 2012

@author: sharath
'''
import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))

from my.Test import exec_command

def testRedirection():
    f = exec_command("echo hi")[0]
    for l in f:
        assert l == "hi"

if __name__ == '__main__':
    testRedirection()
