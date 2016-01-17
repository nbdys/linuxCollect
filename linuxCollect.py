




#subprocess.check_output("ssh machine 1 'your script'")

import os
import sys
import paramiko


# Befehlsliste
befehle = ['hostname', 'date', 'ifconfig', 'whoami']


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())



ssh.connect('192.168.', username='', password='')



for befehl in range(len(befehle)):
    a= befehle[befehl]
    #print a
    stdin, stdout, stderr = ssh.exec_command(a)
    for line in stdout:
        print line.strip('\n')

ssh.close()