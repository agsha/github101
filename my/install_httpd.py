'''
Created on Jun 24, 2012

@author: sharath
'''
from Test import exec_command
from os.path import join, abspath
from os import chdir, getcwd
import re
import os
from os.path import expanduser
DOWNLOAD_DIR = abspath(expanduser("~/Downloads"))
USR_LOCAL = abspath("/usr/local")

HTTPD_URL = "http://www.alliedquotes.com/mirrors/apache//httpd/httpd-2.4.2.tar.gz"


def downloadHttpd():
    exec_command("curl -o httpd-2.4.2.tar.gz -L %s"%HTTPD_URL)
    exec_command("tar xvzf httpd-2.4.2.tar.gz -C %s"%DOWNLOAD_DIR)

if __name__ == '__main__':
    downloadHttpd()