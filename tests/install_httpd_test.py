'''
Created on Jun 17, 2012

@author: sharath
'''
import sys
import os
from my.install_httpd import *
from mock import MagicMock
from mock import patch
import my.install_httpd

l = []
def mock_ex(*args):
    for arg in args:
        l.append(arg)


@patch("my.install_httpd.exec_command", mock_ex)
def testDownloadHttpd():
    downloadHttpd()
    assert len(l) == 2
    assert l[0] == "curl -o httpd-2.4.2.tar.gz -L %s"%HTTPD_URL
    
def allTests():
    testDownloadHttpd()
    
if __name__ == '__main__':
    testDownloadHttpd()