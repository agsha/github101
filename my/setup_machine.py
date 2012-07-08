'''
Created on Jun 27, 2012

@author: sharath
'''
from Test import exec_command
from os.path import join, abspath, expanduser
from os import chdir, getcwd
import re
import os
import install_httpd, install_pip, install_virtualenv, install_py_packages, install_mysql, install_vialogues
DOWNLOAD_DIR = abspath(expanduser("~/Downloads"))
USR_LOCAL = abspath("/usr/local")
    
if __name__ == '__main__':
    install_httpd.main()
    install_pip.main()
    install_virtualenv.main()
    install_py_packages.main()
    install_mysql.main()
    install_vialogues.main()
    
