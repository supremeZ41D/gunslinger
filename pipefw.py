from gunslinger.config import fwscript_cli
from paramiko.client import SSHClient 

def pipefw(sshclient,inlist,vdom=None):
    var2=[]
    if type(inlist) is list:
        for i in inlist:
            if 'config ' in i or 'edit ' in i or 'set ' in i or 'next' in i or 'end' in i:
                if '# ' in i:
                    var2.append(i.split(' # ')[-1])
                    #print(i.split(' # ')[-1].strip('\n'))
                elif 'uuid' in i:
                    continue
                else:
                    var2.append(i)
    else:
        raise RuntimeError("\"inlist\" should be a list!")
        
        
    var2=str(''.join(var2))
    
    if type(sshclient) is list:
        for j in sshclient:
            print("Accessing SSHCLIENT: {}".format(j))
            fwscript_cli(j,var2,vdom=vdom)
    elif type(sshclient) is SSHClient:
        print("Accessing SSHCLIENT: {}".format(sshclient))
        #print('config vdom\nedit {}\n'.format(vdom)+var2)
        fwscript_cli(sshclient,var2,vdom=vdom)
    