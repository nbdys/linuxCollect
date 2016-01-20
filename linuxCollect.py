# -*- coding: utf-8 -*-

import os
import sys
import fabric
import argparse
from fabric.api import *

# Liste der SSH-Hosts initialisieren
rechner=[]

# Liste der Befehle
befehle = ['hostname', 'date', 'uname -a', 'ls -l']

# Parser für Argumente erstellen
parser = argparse.ArgumentParser(description='Sammelt Informationen von Linuxsystemen per SSH', epilog="So zerbroeselt der Keks nunmal...", prog='Linux Collector')

parser.add_argument('-H', dest='hostlist', action="store", help='Pfad zur Hostliste, Format: user@host:Port')
parser.add_argument('target', action="store", help='user@hostname:Port oder user@IP:Port', nargs='?')
parser.add_argument('--version', action='version', version='%(prog)s 0.9beta')

args = parser.parse_args()
argsdict = vars(args)

# Hostliste mit einzelnem Ziel befüllen
if (args.target):
    rechner = [ argsdict['target']]

# Hostliste aus Datei befüllen
elif (args.hostlist):
    datei = open(str([argsdict['hostlist']]), 'rt')
    for line in datei:
        rechner.append(line.rstrip())
    datei.close()

# Wenn keine Argumente übergeben werden die Hilfe aufrufen
else: parser.parse_args(['--help'])


# Hostfile einlesen und in fabfile.py schreiben
"""
def writeFabfile(hostlist, orderlist):
    fabfile = open('fabfile.py','a')
    fabfile.write('from fabric.api import * \n \n')

    fabfile.write('env.hosts = [\n')
    for host in hostlist:
        fabfile.write("'"+host+"'"+'\n')
    fabfile.write(']\n')

    fabfile.write('env.user   = "ssc"\n')

    fabfile.write('def collectSysInfo():\n')
    for befehl in orderlist:
        fabfile.write('\tsudo("'+befehl+'")\n')

    fabfile.close()

writeFabfile(hosts,befehle)
"""

# Befehle für jeden Host abarbeiten und Ausgaben in .html Datei schreiben
if (args.target) or (args.hostliste):
    for h in rechner:
      env.host_string = h

      log = open(h+'.html','a')

      for b in befehle:
          text ="<pre>"+ sudo(b)+"</pre>"
          log.write("<h3>"+b+ "</h3>"+'\n')
          log.write(text.strip('\n'))
          log.write('\n\n')
      log.close()




exit()