#!/usr/bin/env python
# -*- coding: utf-8 -*-

# fixnames-guarda-gde.py  2020 JPV
#
# Este script recorre la guarda documental y arregla las
# cagadas de la migracion de archivos desde S3
#
# Por el momento solo esta implementado el reemplazo del signo + por un espacio.
# Ya se corrio en produccion por lo cual no es necesario correrlo de nuevo
# 
# Quedaria implementar otras cosas que vinieron rotas de esa migracion
# 

import os
import sys
from curses.ascii import isascii
from os.path import walk, join
from os import rename

#Default settings
dirbase="/exports/"
dospaces = False
dodebug = False
doreport = True
domodify = False
enforceillegal = False
trim64 = False
illegalchars = ("*","/",":",";","?","\\","~","$","|")
responsechar = (("+"," "),("%2C",","),("%24","$"),("%25","%"),("%28","("),("%29",")"),("%C3%B3","ó"),\
    ("%C3%81","Á"))

#################### messages
usagemsg = """fixnames - Renames files
Usage: %s directory -s -m -i -r -d

        -m Modify (do the actual mv on disk) 
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
        
        #print nomfile
        #for (chara, charb) in responsechar:
        #    filecorrect=filecorrect.replace(chara,charb)
        #    print filecorrect
        #    print
        filecorrectmp=filecorrect.replace("+"," ")
        #print nomfile,filecorrectmp
        
        if filecorrectmp == filecorrect:
            errorfile = False
        else:
            errorfile = True
            filecorrect = filecorrectmp

        if errorfile == True:
            torename.append((root, nomfile, filecorrect))

 
for (dir, noma, nomb) in torename:
    if doreport == True or dodebug == True:
        print reportmsg % (dir, noma, nomb)

    if domodify == True and len(torename) > 0:
        rename (join(dir , noma), join(dir, nomb))

if domodify == True:
    print "%i Files modified" % (len(torename))
else:
    print "%i Files found (none modified)" % (len(torename))

