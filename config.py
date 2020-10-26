from jinja2 import Environment, FileSystemLoader
import yaml
import gunslinger
import os


class scripts:
    
    def __init__(self,sshclient,path):
        self.sshclient=sshclient
        self.path=path

    def fwscript_txt(self):
        txfile=open(self.path,'r')
        txlist=txfile.readlines()
        stdin,stdout,stderr=self.sshclient.exec_command(''.join(txlist))
        print('SCRIPT PUSHED!')
        txfile.close()
    
    def fwscript_yml(self):
        stdin,stdout,stderr=None,None,None
        
        gunpath=gunslinger.__path__[0]
                
        try:
            os.mkdir('config')
        except FileExistsError:
            pass
        
        try:
            with open('./config/config_file.txt','w') as config:
                config.truncate(0)
        except:
            pass
        
        with open(self.path) as file:
            sjinja=yaml.full_load(file)
        
        env=Environment(loader=FileSystemLoader(gunpath))
        for module in sjinja['global']['modules']:
            tempvar=env.get_template("templates/{}conf.j2".format(module))
            tempconf=tempvar.render(dictvar=sjinja['{}'.format(module)])
            print(tempconf)
            with open('./config/config_file.txt','w') as config:
                config.write(tempconf)
        
        confirm=input('*****Einverstanden?(y/n): ')
        if confirm=='y':
            with open(gunpath+'/config/config_file.txt','r') as config:
                script=config.read()
            
            stdin,stdout,stderr=self.sshclient.exec_command(script)
        
        return stdin,stdout,stderr