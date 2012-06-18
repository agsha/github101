'''
Created on Jun 17, 2012

@author: sharath
'''
import sys
import os
from my.install_mysql import *
import my.Test
from my import Test, install_mysql
from my.Test import exec_command
import my.install_mysql


class Mock(object):
    def __init__(self, commandToMockOut):
        self.old_exec_command = Test.exec_command
        Test.exec_command = self.override_exec_command
        install_mysql.ex = self.override_exec_command
        self.commandToMockOut = commandToMockOut
        self.out = self.err = None
        self.returncode = 0
        
    def override_exec_command (self, command, log=False, errorcheck=True):
        if command == self.commandToMockOut:
            return (self.out, self.err, self.returncode)
        self.good = True
        return self.old_exec_command(command, log, errorcheck)

def testIs64Bit():
    assert is64Bit()

def testMock():
    cmd = "ls -la"
    mock = Mock(cmd)
    e = open(Test.OUT, "w")
    STRING = "typed ls -la"
    e.write(STRING)
    e.close()
    mock.out = open(Test.OUT)
    out = Test.exec_command(cmd)[0]
    for l in out:
        assert l == STRING
    out = Test.exec_command("echo hi")[0]
    for l in out:
        assert l == "hi\n"
    
    
def testMySqlDownloadDir():
    mock = Mock("curl http://dev.mysql.com/get/Downloads/MySQL-5.5/mysql-5.5.25-osx10.6-x86_64.tar.gz/from/http://mysql.mirrors.pair.com/")
    mySqlToDownloadsDir()
    assert mock.good
    
    
    
def allTests():
    testIs64Bit()
    testMock()
    
if __name__ == '__main__':
    testMySqlDownloadDir()