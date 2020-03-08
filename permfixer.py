#!/usr/bin/env python

# Permfixer 1.0

import os
import sys
import stat
dofiles = False

dirbase="/home/jpv/misfiles/test"

if len(sys.argv) > 1:
    
    for argu in sys.argv[1:]:
        if argu == "-f":
            dofiles = True
            
    if os.path.isdir(sys.argv[1]) == True:
        dirbase = sys.argv[1]
        print "Using %s as basedir" % (dirbase)
else:
    print "Using %s as basedir (default)" % (dirbase)
    


for root, dirs, files in os.walk(dirbase):
    
    if dofiles == True:
        for nomfile in files:
            st = os.stat(os.path.join (root, nomfile))
            
            if oct(stat.S_IMODE(st[stat.ST_MODE])) != "0644":
                os.system("chmod 644 \"" + os.path.join (root, nomfile)+"\"")
                print "Tocando %s" % (nomfile)
            
    for nomdir in dirs:
        st = os.stat(os.path.join (root, nomdir))
        
        if oct(stat.S_IMODE(st[stat.ST_MODE])) != "0755":
            os.system("chmod 755 \"" + os.path.join (root, nomdir)+"\"")
            print "Tocando %s" % (nomdir)
