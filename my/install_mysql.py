'''
Created on Jun 17, 2012

@author: sharath
'''

from Test import exec_command as ex
from os.path import join, abspath
from os import chdir, getcwd
import re
import os
from os.path import expanduser
DOWNLOAD_DIR = abspath(expanduser("~/Downloads"))
MYSQL_64_URL = "http://dev.mysql.com/get/Downloads/MySQL-5.5/mysql-5.5.25-osx10.6-x86_64.tar.gz/from/http://mysql.mirrors.pair.com/"
MYSQL_32_URL = "http://dev.mysql.com/get/Downloads/MySQL-5.5/mysql-5.5.25-osx10.5-x86.tar.gz/from/http://mysql.mirrors.pair.com/"
USR_LOCAL = abspath("/usr/local")
def is64Bit():
    out = ex("uname -a")[0]
    for line in out:
        if re.match(".*RELEASE_X86_64 x86_64$", line) is not None:
            return True
        elif re.match(".*RELEASE_I386 i386$", line) is not None:
            return False
        else:
            raise Exception("Cant detect if cpu is 32 bit or 64 bit")

def mySqlToDownloadsDir():
    chdir(DOWNLOAD_DIR)
    url = MYSQL_32_URL
    if is64Bit():
        url = MYSQL_64_URL
    ret = ex("curl -o mysql-5.5.25-osx10.6-x86_64.tar.gz -L %s"%url, errorcheck=False)
    for l in ret[1]:
        print "errorsdf %s"%l
    ex("sudo tar xvzf mysql-5.5.25-osx10.6-x86_64.tar.gz -C %s"%USR_LOCAL)
    ex("sudo ln -s mysql-5.5.25-osx10.6-x86_64.tar.gz %s/mysql"%USR_LOCAL)

if __name__ == '__main__':
    mySqlToDownloadsDir()
