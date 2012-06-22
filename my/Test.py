'''
Created on Apr 23, 2012

@author: sharath
'''
import os, sys
import subprocess
import re
import os.path
import __builtin__
from os.path import join
from os.path import abspath

class Unbuffered:
    def __init__( self, stream ):
        self.stream = stream
    def write( self, data ):
        self.stream.write( data )
        self.stream.flush()
    def __getattr__( self, attr ):
        return getattr( self.stream, attr )
sys.stdout=Unbuffered(sys.stdout)

def open(filename, mode="r"):
    return Unbuffered(__builtin__.open(filename, mode))

BITBUCKET_FOLDER = os.path.abspath(".")
ERR = os.path.join(os.getcwd(), "err")
OUT = os.path.join(os.getcwd(), "out")
AUTHORS_FILE = os.path.join(BITBUCKET_FOLDER, "users.txt")
apps = {
#        "configurations":"git clone git@bitbucket.org:edlab/unknown-configurations.git",
         "documentation": "git@bitbucket.org:edlab/unknown-documentation.git",
#        "eddais":"git@bitbucket.org:edlab/apps-eddais.git",
#        "edlabauth":"git@bitbucket.org:edlab/apps-edlab-cas.git",
#        "identity": "git@bitbucket.org:edlab/apps-cas-main-code.git",
#        "library": "git@bitbucket.org:edlab/library-library-website.git",
#        #"mschool":"",
#        #"netposse":"",
#        #"oauth":"",
#        #"ojs":"",
#        #"slms":"",
#        #"tclibrary":"",
          "tcrsearch":"git@bitbucket.org:edlab/publications-tc-record.git",
#        "timesheet":"git@bitbucket.org:edlab/library-time-sheet-tool.git",
#        "twitterSymposium":"git@bitbucket.org:edlab/library-twitter-symposium.git",
#        "young_arts":"git@bitbucket.org:edlab/publications-young-arts-website.git",
#        "NLT_CMS":"git@bitbucket.org:edlab/new-learning-times-cms.git",
#        #"plugins":"",
        }
# get a unique ID for this 
i = 0
path = BITBUCKET_FOLDER+"ID"
if os.path.exists(path):
    i = int(open(path).readline())
f = open(path, "w")
f.writelines(str(i+1))
f.close()

def exec_command(command, log=False, errorcheck=True):
    if log : 
        route = "(%s 2>&1 1>&3 | tee -a stderr.txt | tee %s ) 3>&1 1>&2 | tee -a stdout.txt | tee %s"%(command, ERR, OUT)
    else:
        route = "(%s 2>&1 1>&3 | tee %s ) 3>&1 1>&2 | tee %s"%(command, ERR, OUT)
    print("[[%s]]\n"%route)
    proc = subprocess.Popen(route, shell=True)
    proc.wait()
    if errorcheck and proc.returncode!=0:
        raise Exception("return code is not zero")
    for l in open(ERR) :
        print "WARNING: error file not empty: %s"%l
    return (open(OUT), open(ERR), proc.returncode)

def getdirs(out, err, returncode):
    l = []
    p = re.compile("^d[\S]*[\s]+[\S]*[\s]+[\S]*[\s]+[\S]*[\s]+[\S]*[\s]+[\S]*[\s]+[\S]*[\s]+(?P<dir>.*)$")
    for line in out:
        m = p.match(line)
        if m!=None:
            l.append( m.group("dir"))
    return l        
    
def MissingAuthorConsumer(out, err, returncode):
    m = None
    pat = re.compile(r"^\n?Author: (?P<author>[a-zA-Z0-9_-]*) not defined in [a-zA-Z0-9/\.]* file\n?$")
    for line in err:
        m = pat.match(line)
        break
    if (m == None and returncode!=0):
        raise Exception("[[script]] Command failed.")
    if m is not None:
        return m.group("author")
    else:
        return m

def RemoteAdded(out, err, returncode):
    for line in out:
        if line.startswith("origin"):
            return True
    return False


def _updateexcel(dir):
    pass


def isNull(string):
    if string == "":
        return False
    else: 
        return True
  


        
def main():
    for app in apps :
        print "======================================"
        print "     Running script for %s"%app
        print "======================================"
        try:
            folder = os.path.join(BITBUCKET_FOLDER, app)
            os.chdir(BITBUCKET_FOLDER)
            if not os.path.exists(folder) :
                exec_command("mkdir %s" % folder, errorcheck = False)
            os.chdir(folder)
            open(AUTHORS_FILE, "a").close()
            while True:
                if not os.path.exists(os.path.join(folder, ".git/")) :
                    author = MissingAuthorConsumer(*exec_command("git svn clone svn+ssh://sha@admin-edlab.tc.columbia.edu/var/svn/%s --authors-file=%s --no-metadata -s %s"%(app, AUTHORS_FILE, folder), errorcheck=False,))
                else :
                    author = MissingAuthorConsumer(*exec_command("git svn fetch", errorcheck = False))
                if author is None or len(author) == 0:
                    break
    
                authorsFile = open(AUTHORS_FILE, "a")
                authorsFile.writelines("%s = %s <edlabit+%s@tc.columbia.edu>\n"%(author, author, author))
                authorsFile.close()
            exec_command("cp -Rf .git/refs/remotes/tags/* .git/refs/tags/", errorcheck=False)
            exec_command("find .git/refs/remotes/ -type f -not  -name  *trunk*   -exec mv {} .git/refs/heads/ \;", errorcheck=False)
            good = RemoteAdded(*exec_command("git remote -v"))
            if good != True:
                exec_command("git remote add origin %s"%apps[app])
                
            val = exec_command("git push origin --all", errorcheck=False)
            for l in val[1]:
                if re.match("^[\w]*Everything up-to-date[\w]*$", l) is None:
                    raise Exception("Error occured in git push origin --all")
        except Exception:
            pass


def tar():
    tardir = os.path.join(os.path.abspath("/home/sha/"), "tar")
    exec_command("mkdir %s" % tardir)
    for dr in os.listdir("/var/trac/sites/"):
        exec_command("tar -cvf %s %s"%(os.path.join(tardir, dr+".tar"), os.path.join("/var/trac/sites/", dr)))
    
    
    
def dummy():
    print "please enter a method name to run like so: python Test.py main" 
       
if __name__ == '__main__':
    method = 'main'
    if len(sys.argv) > 1 :
        method = sys.argv[1] 
        globals()[sys.argv[1]]()
    else:
        main()    