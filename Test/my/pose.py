'''
Created on Jun 14, 2012

@author: sharath
'''

COLFILE = ""
TABNAME = ""
NEWTABNAME = ""
if __name__ == '__main__':
    l = []
    for line in open(COLFILE):
      l.append(line)
    columns = "\t".join(l)
    
    f = open(NEWTABNAME)
    f.write(columns)
    for line in open(TABNAME):
      f.write(line)
    f.close()

    