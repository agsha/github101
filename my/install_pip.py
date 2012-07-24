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

PIP_URL = "http://pypi.python.org/packages/source/p/pip/pip-1.1.tar.gz"
PIP_DIR = "pip-1.1"

def _downloadPip():
    chdir(DOWNLOAD_DIR)
    exec_command("curl -o pip-1.1.tar.gz -L %s"%PIP_URL)
    
def _extractPip():
    chdir(DOWNLOAD_DIR)
    exec_command("tar xvzf pip-1.1.tar.gz -C %s"%DOWNLOAD_DIR)
    chdir(join(DOWNLOAD_DIR, PIP_DIR))
    exec_command("sudo python setup.py install")

def main():    
    _downloadPip()
    _extractPip()

if __name__ == '__main__':
    main()