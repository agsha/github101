'''
Created on Apr 23, 2012

@author: sharath
'''
import os, sys
import subprocess
import re

BITBUCKET_FOLDER = os.path.abspath(".")
AUTHORS_FILE = os.path.join(BITBUCKET_FOLDER, "users.txt")
apps = {"researched":"git@bitbucket.org:edlab/apps-research-broker.git"}
LINE_BUFFERED = 1
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
        route = "(%s 2>&1 1>&3 | tee -a stderr.txt | tee err ) 3>&1 1>&2 | tee -a stdout.txt | tee out"%command
    else:
        route = "(%s 2>&1 1>&3 | tee err ) 3>&1 1>&2 | tee out"%command
    print("[[%s]]\n"%route)
    proc = subprocess.Popen(route, shell=True)
    proc.wait()
    if errorcheck:
        if proc.returncode!=0:
            raise Exception("return code is not zero")
        for l in open("err") :
            raise Exception("Error file not empty")
    return (open("out"), open("err"), proc.returncode)

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
    if (m == None and returncode!=0):
        raise Exception("[[script]] Command failed.")
    return m

def RemoteAdded(out, err, returncode):
    for line in out:
        if line.startswith("origin"):
            return True
    return False


def _updateexcel(dir):
  pass


def populategoogleexcel():
    p = os.path.abspath("/home/sha/bitbucket")
    l = getdirs(*exec_command("ls -l %s | grep ^d" % p))
    
    for d in l:
        os.chdir(os.path.join(p, d))
        if RemoteAdded(*exec_command("git remote -v")):
            _updateexcel(dir=d)

def isNull(string):
  if string == "":
    return False
  else: 
    return True
  


        
def main():
    for app in apps :
        folder = os.path.join(BITBUCKET_FOLDER, app)
        os.chdir(BITBUCKET_FOLDER)
        print "printing folderrr" + folder
        print "prinnting git" + os.path.join(folder, ".git/")
        if not os.path.exists(folder) :
            exec_command("mkdir %s" % folder, errorcheck = False)
        os.chdir(folder)
        open(AUTHORS_FILE, "a").close()
        while True:
            try:
                if not os.path.exists(os.path.join(folder, ".git/")) :
                    author = MissingAuthorConsumer(*exec_command("git svn clone svn+ssh://sha@admin-edlab.tc.columbia.edu/var/svn/%s --authors-file=%s --no-metadata -s %s"%(app, AUTHORS_FILE, folder), errorcheck=False,))
                else :
                    author = MissingAuthorConsumer(*exec_command("git svn fetch", errorcheck = False))
            except Exception:
                pass
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
        dummy()    