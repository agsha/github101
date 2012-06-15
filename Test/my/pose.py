'''
Created on Jun 14, 2012

@author: sharath
'''
import subprocess
import os

COLFILE = "col.txt"
TABNAME = "row.txt"
NEWTABNAME = "join.txt"
SEPARATOR = "\t"

ERR = os.path.join(os.getcwd(), "err")
OUT = os.path.join(os.getcwd(), "out")

def exec_command(command, log=False, errorcheck=True):
    if log : 
        route = "(%s 2>&1 1>&3 | tee -a stderr.txt | tee %s ) 3>&1 1>&2 | tee -a stdout.txt | tee %s"%(command, ERR, OUT)
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

if __name__ == '__main__':
    l = []
    for line in open(COLFILE):
      l.append(line)
    columns = SEPARATOR.join(l)
    
    f = open(NEWTABNAME, "w")
    f.write(columns+"\n")
    for line in open(TABNAME):
      f.write(line)
    f.close()

    