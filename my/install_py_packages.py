'''
Created on Jun 27, 2012

@author: sharath
'''
from Test import exec_command
from os.path import join, abspath, expanduser
from os import chdir, getcwd
import re
import os

DOWNLOAD_DIR = abspath(expanduser("~/Downloads"))
USR_LOCAL = abspath("/usr/local")

def _installDjango():
    exec_command("sudo pip install Django")

def _installHayStack():
    exec_command("sudo pip install django-haystack")

def _installMySqlDb():
    exec_command("sudo pip install MySQL-python")
    exec_command("sudo ln -s /usr/local/mysql/lib/libmysqlclient.18.dylib /usr/lib/libmysqlclient.18.dylib")

def _installPySolr():
    exec_command("sudo pip install pysolr")

def _installBoto():
    exec_command("sudo pip install boto")

def _installPiston():
    exec_command("sudo pip install django-piston")    

def _installPyCrypto():
    exec_command("sudo pip install pycrypto")

def _installSimpleJson():
    exec_command("sudo pip install simplejson")
    
if __name__ == '__main__':
    _installDjango()
    _installHayStack()
    _installMySqlDb()
    _installPySolr()
    _installBoto()
    _installPiston()
    _installSimpleJson()
