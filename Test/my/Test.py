'''
Created on Apr 23, 2012

@author: sharath
'''
import os, sys
import subprocess
import re


BITBUCKET_FOLDER = os.path.abspath(".")
AUTHORS_FILE = os.path.join(BITBUCKET_FOLDER, "users.txt")
apps = {"django-lib":"git@bitbucket.org:edlab/apps-django-cas.git"}
LINE_BUFFERED = 1
# get a unique ID for this 
i = 0
path = BITBUCKET_FOLDER+"ID"
if os.path.exists(path):
    i = int(open(path).readline())
f = open(path, "w")
f.writelines(str(i+1))
f.close()

class NullConsumer(object):
    def begin(self):
        pass
    def end(self):
        pass
    def write(self, line):
        pass

def exec_command(command, consumer = NullConsumer()):
    print("[[%s]]\n"%command)
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=LINE_BUFFERED)
    proc.wait()
    consumer.begin()
    for line in proc.stdout:
        sys.stdout.write(line)
        consumer.write(line)
    for line in proc.stderr:
        sys.stderr.write(line)
        consumer.write(line)
    consumer.end()
    if proc.returncode != 0:
        raise Exception("failed!")
    return proc


class MissingAuthorConsumer(object):
    def begin(self):
        self.author = []
        self.pat = re.compile(r"^\n?Author: (?P<author>[a-zA-Z0-9_-]*) not defined in [a-zA-Z0-9/\.]* file\n?$")
    def end(self):
        pass
    def write(self, line):
        m = self.pat.match(line)
        if m != None:
            self.author.append(m.group("author"))

class RemoteAdded(object):
    def begin(self):
        self.remote = False
    def end(self):
        pass
    def write(self, line):
        self.remote = True
        if line.startswith("origin") == False:
            self.remote = False
   
def main():
    for app in apps :
        folder = os.path.join(BITBUCKET_FOLDER, app)
        os.chdir(BITBUCKET_FOLDER)
        print "printing folderrr" + folder
        print "prinnting git" + os.path.join(folder, ".git/")
        if not os.path.exists(folder) :
            exec_command("mkdir %s" % folder)
        os.chdir(folder)
        open(AUTHORS_FILE, "a").close()
        while True:
            missingAuthorConsumer = MissingAuthorConsumer()
            try:
                if not os.path.exists(os.path.join(folder, ".git/")) :
                    proc = exec_command("git svn clone svn+ssh://sha@admin-edlab.tc.columbia.edu/var/svn/%s --authors-file=%s --no-metadata -s %s"%(app, AUTHORS_FILE, folder), consumer=missingAuthorConsumer)
                else :
                    proc = exec_command("git svn fetch", consumer=missingAuthorConsumer)
            except Exception:
                pass
            if len(missingAuthorConsumer.author) == 0:
                break
            authorsFile = open(AUTHORS_FILE, "a")
            for author in missingAuthorConsumer.author:
                authorsFile.writelines("%s = %s <edlabit+%s@tc.columbia.edu>\n"%(author, author, author))
            authorsFile.close()
        try :
            exec_command("cp -Rf .git/refs/remotes/tags/* .git/refs/tags/")
        except Exception:
            pass
        try :
            exec_command("find .git/refs/remotes/ -type f -not  -name  *trunk*   -exec mv {} .git/refs/heads/ \;")
        except Exception:
            pass
        remoteAdded = RemoteAdded()
        exec_command("git remote -v", consumer = remoteAdded)
        if remoteAdded.remote != True:
            exec_command("git remote add origin %s"%apps[app])
        exec_command("git push origin --all")

def tar():
    tardir = os.path.join(os.path.abspath("/home/sha/"), "tar")
    exec_command("mkdir %s" % tardir)
    for dr in os.listdir("/var/trac/sites/"):
        exec_command("tar -cvf %s %s"%(os.path.join(tardir, dr+".tar"), os.path.join("/var/trac/sites/", dr)))
    
    
    
    
if __name__ == '__main__':
    method = 'main'
    if len(sys.argv) > 1 :
        method = sys.argv[1] 
        globals()[sys.argv[1]]()
    else:
        main()    