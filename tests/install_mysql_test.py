'''
Created on Jun 17, 2012

@author: sharath
'''
import sys
import os
from Test.my.install_mysql import *
from Test.my.Tes
class Mock(object):
    def __init__(self):
        self.old_exec_command = exec_command
        exec_command = self.override_exec_command
        
    def override_exec_command (self, command, log=False, errorcheck=True):
        self.command = command
        return (self.out, self.err, self.returncode)

mock = Mock()
exec_command = mock.override_exec_command
def testIs64Bit():
    assert is64Bit()

def testMySqlToDownloadsDir():
    assert os.getcwd() == os.path.expanduser("~/Downloads")
    assert mock.command == "wget %s"%url
    
if __name__ == '__main__':
    testIs64Bit()