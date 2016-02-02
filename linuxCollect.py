# -*- coding: utf-8 -*-

import argparse
from fabric.api import *
from fabric.exceptions import NetworkError

# Liste der SSH-Hosts initialisieren
rechner = []
# ToDo: Mit Schalter aufteilen nach Grundbefehlen und erweiterteten Befehlen
# Liste der Befehle
commands = []

def readCommands(c):
   # print c  # just for debug
    datei = open(str(c), 'rt')
    for line in datei:
        commands.append(line.strip())
    datei.close()
    # print commands  # debug 2

def readTarget(t):
    for target in t:
        rechner.append(target)
    #print t

## ToDo: Abfangen, wenn die letzte Zeile der Liste ein Enter am Ende hat
def readHostlist(h):
    datei = open(str(h), 'rt')
    for line in datei:
        rechner.append(line.rstrip())
    datei.close()


# Parser für Argumente erstellen
parser = argparse.ArgumentParser(description='Sammelt Informationen von Linuxsystemen per SSH',
                                 epilog="So zerbroeselt der Keks nunmal...", prog='Linux Collector')

parser.add_argument('-d', '--datei', dest='hostlist', action="store", help='Pfad zur Hostliste, Format: user@host:Port')
parser.add_argument('-t', '--target', dest='target', action="store",
                    help='user@hostname:Port oder user@IP:Port, mehrere moeglich', nargs='*')
parser.add_argument('-c', '--commands', dest='commandl', action='store')
parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.9beta')

args = parser.parse_args()
argsdict = vars(args)

# Hostliste mit einzelnem Ziel befüllen
if (args.target):
    readTarget(argsdict['target'])

# Hostliste aus Datei befüllen
if(args.hostlist):
    readHostlist(argsdict['hostlist'])

if (args.commandl):
	readCommands(argsdict['commandl'])

# Wenn keine Argumente übergeben werden die Hilfe aufrufen
else:
    parser.parse_args(['--help'])

# Hostfile einlesen und in fabfile.py schreiben TODO: Schalter implementieren
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

writeFabfile(hosts,commands)
"""

# Befehle für jeden Host abarbeiten und Ausgaben in .html Datei schreiben
if (args.target) or (args.hostlist):
    print rechner
    for h in rechner:
        env.host_string = h  # Host zu dem die Verbindung aufgebaut wird
        env.warn_only = True  # Nur Warnungen zeigen, nicht das Programm abbrechen
        env.skip_bad_hosts = True  # Hosts überspringen, welche nicht erreichbar sind
        env.timeout = '60'
        print h
        log = open(h + '.html', 'a')  # Logdatei erstellen und oeffnen
        log.write(' <!-- HTML 4.x --> <meta http-equiv="content-type" content="text/html; charset=utf-8"> <!-- HTML5 --> <meta charset="utf-8">')
        for b in commands:
            try:
                result = sudo(b)
		# print b
                if result.return_code != 0:
                    continue
                else:
                    text = "<pre>" +result + "</pre>"
                    log.write("<h3>" + b + "</h3>" + '\n')
                    log.write(text.strip('\n'))
                    log.write('\n\n')
            except NetworkError as e:  # SSH Connection Refused abfangen
                print e
                break

        log.close()

exit()
