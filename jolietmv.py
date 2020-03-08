#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Jolietmv 1.0
#

import os
import sys
from curses.ascii import isascii
from os.path import walk, join
from os import rename

#Default settings
dirbase="/home/jpv/misfiles/"
dospaces = False
dodebug = False
doreport = True
domodify = False
enforceillegal = True
trim64 = False
illegalchars = ("*","/",":",";","?","\\","~","$","|")
responsechar = (("á","a"),("é","e"),("í","i"),("ó","o"),("ú","u"),("ñ","n"),\
    ("Ñ","N"))

#################### messages
usagemsg = """JolietMv - Renames files to conform Joliet standard
Usage: %s directory -s -m -i -r -d

        -s Check for spaces and replace them with underscores
        -m Modify (do the actual mv on disk)
        -i Enforce illegal Joliet characters "?/\*:?" and replace them with an Z
        -t Trim files and dirs to 64 characters max 
        -d Debug mode
        -h this message

""" % (sys.argv[0])

errmensaje = """ANOMALY DETECTED -------
    Error: %s
    Found in: %s
    Location: %s
    Renamed to: %s
    -----------------
    
    """

reportmsg = """+-----------------------------------------
| Folder: %s 
| Rename:
|         %s
|            to
|         %s
+-----------------------------------------"""
####################### end messages

if len(sys.argv) > 1:
    
    for argu in sys.argv[1:]:
        if argu == "-h":
            print usagemsg
            sys.exit
        if argu == "-m":
            domodify = True
        if argu == "-d":
            dodebug = True
        if argu == "-s":
            dospaces = True
        if argu == "-t":
            trim64 = True
        if argu == "-i":
            enforceillegal = True
    
    if os.path.isdir(sys.argv[1]) == True:
        dirbase = sys.argv[1]
        print "Using %s as basedir" % (dirbase)
    
else:
    print "Using %s as basedir (default)" % (dirbase) 

#this list holds all changes
torename=[]

#Main loop walk --this is what makes it tick--
for root, dirs, files in os.walk(dirbase):

    for nomfile in files:
        filecorrect = nomfile
        errorfile = False
        
        for letrasfile in nomfile:

            if dospaces == True:   
                if letrasfile == " ":
                    filecorrect = filecorrect.replace(" ", "_")
                    errorfile = True
            
            if enforceillegal == True:   
                for i in illegalchars:
                    if letrasfile == i:
                        filecorrect = filecorrect.replace(i, "Z")
                        errorfile = True
                    
            if not isascii(letrasfile):
                errorfile = True
                for (chara, charb) in responsechar:
                    if letrasfile == chara:
                        filecorrect == filecorrect.replace(chara, charb)
                    
                filecorrect = filecorrect.replace(letrasfile, "X")
                
                if dodebug == True:
                    msg = "Illegal character (" + letrasfile +")"
                    print errmensaje % (msg, nomfile, root, filecorrect)
                    
        if len(nomfile) >= 64 and trim64 ==True:
            filecorrect = filecorrect[0:50]+ "__" + filecorrect[-11:]
            errorfile = True
            
            if dodebug == True:
                msg = "Filename long than 64 characters"
                print errmensaje % (msg, nomfile, root, filecorrect) 
                
        if errorfile == True:
            torename.append((root, nomfile, filecorrect))
            
     
    for nomdir in dirs:
        dircorrect = nomdir
        errordir = False
     
        for letrasdir in nomdir:
            
            if dospaces == True:
                if letrasdir == " ":
                    dircorrect = dircorrect.replace(" ", "_")
                    errordir = True
            
            if enforceillegal == True:
                for i in illegalchars:
                    if letrasdir == i:
                        dircorrect = dircorrect.replace(i, "Z")
                        errordir = True
            
            if not isascii(letrasdir):
                errordir = True
                for (chara, charb) in responsechar:
                    if letrasdir == chara:
                        dircorrect == dircorrect.replace(chara, charb)
                dircorrect = dircorrect.replace(letrasdir, "X")
                
                if dodebug == True:
                    msg = "Illegal character (" + letrasdir +")"
                    print errmensaje % (msg, nomdir, root, dircorrect)
        
        if len(nomdir) >= 64 and trim64 == True:
            dircorrect = dircorrect[0:63]
            errordir = True
            
            if dodebug == True:
                msg = "Filename long than 64 characters"
                print errmensaje % (msg, nomdir, root, dircorrect) 
                
        if errordir == True:
            torename.append((root, nomdir, dircorrect))

for (dir, noma, nomb) in torename:
    if doreport == True or dodebug == True:
        print reportmsg % (dir, noma, nomb)

    if domodify == True and len(torename) > 0:
        rename (join(dir , noma), join(dir, nomb))

if domodify == True:
    print "%i Files modified" % (len(torename))
else:
    print "%i Files found (none modified)" % (len(torename))
