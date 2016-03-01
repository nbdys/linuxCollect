#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from fabric.api import *
from fabric.exceptions import NetworkError

# Liste der SSH-Hosts initialisieren
rechner = []
# ToDo: Mit Schalter aufteilen nach Grundbefehlen und erweiterteten Befehlen
# Liste der Befehle
commands = []


# noinspection PyPep8Naming
def readCommands(c):
    print c
    datei = open(str(c), 'rt')
    for line in datei:
        commands.append(line.strip())
    datei.close()


# noinspection PyPep8Naming
def readTarget(t):
    for target in t:
        rechner.append(target)


# ToDo: Abfangen, wenn die letzte Zeile der Liste ein Enter am Ende hat

# noinspection PyPep8Naming
def readHostlist(h):
    datei = open(str(h), 'rt')
    for line in datei:
        rechner.append(line.rstrip())
    datei.close()


def createFile(h):
    log = open(h + '.html', 'a')
    log.write(' <!-- HTML 4.x --> <meta http-equiv="content-type" content="text/html; ''charset=utf-8"> <!-- HTML5 --> <meta charset="utf-8">')
    log.write('<h1>' + h + '</h1>')
    log.write('<ul>')
    i = 1
    for b in commands:
        log.write('<li><a href="#' + str(i) + ' ">' + b + '</a></li>')
        i = i + 1
    log.write('</ul>')
    log.close


def writeLog(name, header, content):
    log = open(name, 'a')
    log.write(header)
    log.write(content)
    log.write('\n\n')
    log.close


# Parser für Argumente erstellen
parser = argparse.ArgumentParser(
    description='remote command exec via SSH', epilog="So zerbroeselt der Keks nunmal...", prog='Linux Collector')
parser.add_argument('-t', '--target', dest='target', action="store",
                    help='user@hostname:Port oder user@IP:Port, mehrere moeglich', nargs='*')
parser.add_argument('-T', '--targetlist', dest='hostlist', action="store",
                    help='Pfad zur Hostliste, Format: user@host:Port')
parser.add_argument('-c', '--command', dest='command', action='store')
parser.add_argument('-C', '--commandlist', dest='commandl', action='store')
parser.add_argument('-a', '--aktComp', dest='ak', action='store')

parser.add_argument(
    '-v', '--version', action='version', version='%(prog)s 0.9beta')

args = parser.parse_args()
argsdict = vars(args)

# Hostliste mit einzelnem Ziel befüllen
if (args.target):
    readTarget(argsdict['target'])

# Hostliste aus Datei befüllen
if (args.hostlist):
    readHostlist(argsdict['hostlist'])

if (args.commandl):
    readCommands(argsdict['commandl'])


if (args.command):
    readCommands(argsdict['command'])

# Wenn keine Argumente übergeben werden die Hilfe aufrufen
else:
    parser.parse_args(['--help'])


# Befehle für jeden Host abarbeiten und Ausgaben in .html Datei schreiben
if (args.hostlist) or (args.target):
    for h in rechner:
        print h
        env.host_string = h  # Host zu dem die Verbindung aufgebaut wird
        # Nur Warnungen zeigen, nicht das Programm abbrechen
        env.warn_only = True
        # Hosts überspringen, welche nicht erreichbar sind
        env.skip_bad_hosts = True
        env.timeout = '60'
        # Logdatei als .html-Datei erstellen
        createFile(h)

        i = 0
        for b in commands:
            i = i + 1
            try:
                result = sudo(b)

                if result.return_code != 0:  # Error nicht loggen
                    continue

                else:
                    header = '<h2 id="' + str(i) + '">' + b + '</h2>' + '\n'
                    content = "<pre>" + result + "</pre>"
                    content = (content.strip('\n'))
                    dateiName = h + ".html"
                    writeLog(dateiName, header, content)

            except NetworkError as e:  # SSH Connection Refused abfangen
                print e
                break
exit()
