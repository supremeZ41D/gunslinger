from jinja2 import Environment, FileSystemLoader
import yaml
from gunslinger.manage import access, close
from getpass import getpass
from gunslinger import validation

def fwscript_txt(sshclient, path='C:/Users/omar.brito/Documents/Python_Security_Exercises/Plantilla SOC 17-10-2018.txt'):
    txfile=open(path,'r')
    txlist=txfile.readlines()
    stdin,stdout,stderr=sshclient.exec_command(''.join(txlist))
    print('SCRIPT PUSHED!')
    txfile.close()

