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
PCRE_URL = "ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.20.tar.gz"
HTTPD_URL = "http://www.alliedquotes.com/mirrors/apache//httpd/httpd-2.4.2.tar.gz"
PCRE_DIR = "pcre-8.20"
HTTPD_DIR = "httpd-2.4.2"
MOD_WSGI_URL = "http://modwsgi.googlecode.com/files/mod_wsgi-3.3.tar.gz"
MOD_WSGI_DIR = "mod_wsgi-3.3"

def downloadHttpd():
    chdir(DOWNLOAD_DIR)
    exec_command("curl -o httpd-2.4.2.tar.gz -L %s"%HTTPD_URL)

def _extractHttpd():
    chdir(DOWNLOAD_DIR)
    exec_command("tar xvzf httpd-2.4.2.tar.gz -C %s"%DOWNLOAD_DIR)
    chdir(join(DOWNLOAD_DIR, HTTPD_DIR))
    exec_command("%s --prefix=%s"%(join(DOWNLOAD_DIR, HTTPD_DIR, "configure"), join(USR_LOCAL, "apache2")))
    exec_command("make")
    exec_command("sudo make install")
    exec_command('echo "export PATH=\\$PATH:%s" >> ~/.profile'%join(USR_LOCAL, "apache2", "bin"))

def _downloadPcre():
    chdir(DOWNLOAD_DIR)
    exec_command("curl -o pcre-8.20.tar.gz -L %s"%PCRE_URL)
    
def _extractPcre():
    chdir(DOWNLOAD_DIR)
    exec_command("tar xvzf pcre-8.20.tar.gz -C %s"%( DOWNLOAD_DIR))
    chdir(join(DOWNLOAD_DIR, PCRE_DIR))
    exec_command("%s --prefix=%s"%(join(DOWNLOAD_DIR, PCRE_DIR, "configure"), join(USR_LOCAL, PCRE_DIR)))
    exec_command("make")
    exec_command("sudo make install")
    exec_command('echo "export PATH=\\$PATH:%s" >> ~/.profile'%join(USR_LOCAL, PCRE_DIR, "bin"))

def _downloadModWsgi():
    chdir(DOWNLOAD_DIR)
    exec_command("curl -o mod_wsgi-3.3.tar.gz -L %s"%MOD_WSGI_URL)

def _extractModWsgi():
    chdir(DOWNLOAD_DIR)
    exec_command("tar xvzf mod_wsgi-3.3.tar.gz -C %s"%( DOWNLOAD_DIR))
    chdir(join(DOWNLOAD_DIR, MOD_WSGI_DIR))
    exec_command("%s"%(join(DOWNLOAD_DIR, MOD_WSGI_DIR, "configure")))
    exec_command("make")
    exec_command("sudo make install")
    
    

if __name__ == '__main__':
    #downloadHttpd()
    _downloadModWsgi()
    _extractModWsgi()