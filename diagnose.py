from gunslinger import validation
from gunslinger.disclose import storeprint, vdomfunc

def commit(sshclient, paramlist):
    stdin,stdout,stderr=sshclient.exec_command('\n'.join(paramlist)+'\n')
    #print(stdin.readlines())
    #print(stdout.readlines())
    print('SCRIPT PUSHED!')
    for i in stdout.readlines():
        print(i.strip('\n'))

class hardware_info:

    def __init__(self, sshclient):
        self.sshclient=sshclient

    def set(self, name=None, option='print'):

        if not name:
            print('PLEASE ENTER AN INTERFACE VALUE!')
        else:
            if validation.globval(self.sshclient):
                if validation.intval(self.sshclient,name):
                    paramlist=['diagnose hardware deviceinfo nic {}'.format(name)]
                else:
                    print('\"{}\" is not in the physical interfaces list!'.format(name))
            else:
                if validation.intval(self.sshclient,name):
                    paramlist=['config global','diagnose hardware deviceinfo nic {}'.format(name)]
                else:
                    print('\"{}\" is not in the physical interfaces list!'.format(name))

        try:
            return storeprint(self.sshclient,paramlist,option)
        except:
            print('Incorrect VDOM/GLOBAL!')


class sys_ha_checksum_cluster:
    
    def __init__(self, sshclient):
        self.sshclient=sshclient
    
    def set(self, flt='',option='print'):
        precomm="""config global
        """
        command="""diagnose sys ha checksum cluster
        """
        
        stdout=vdomfunc(self.sshclient,'global', precomm, command)
        return storeprint(stdout,option)

class sys_session:

    set_src=None
    set_dst=None
    set_dport=None

    def __init__(self, sshclient):
        self.sshclient=sshclient

    def clear_all():

        sys_session.set_src=None
        sys_session.set_dst=None
        sys_session.set_dport=None

    def set(self, vdom=None, flt=''):

        params= {
            'src': sys_session.set_src,
            'dst': sys_session.set_dst,
            'dport': sys_session.set_dport
            }

        if not vdom:
            paramlist=['diagnose sys session filter clear']
            for i in params:
                if params[i]:
                    paramlist.append('diagnose sys session filter {} {}'.format(i,params[i]))
        elif validation.vdomval(self.sshclient,vdom):
            paramlist=['config vdom','edit {}'.format(vdom),'diagnose sys session filter clear']
            for i in params:
                if params[i]:
                    paramlist.append('diagnose sys session filter {} {}'.format(i,params[i]))

        paramlist.append('diagnose sys session list {}'.format(flt))

        try:
            commit(self.sshclient,paramlist)
        except:
            print('Incorrect VDOM/GLOBAL!')


class exec_ping:

    set_src=None
    set_repeat=None
    set_size=None

    def __init__(self, sshclient):
        self.sshclient=sshclient

    def clear_all():

        exec_ping.set_src=None
        exec_ping.set_repeat=None
        exec_ping.set_size=None

    def set(self, dst, vdom=None):

        if not dst:
            print('PLEASE ENTER A DESTINATION VALUE!')
        else:
            params= {
                'source': exec_ping.set_src,
                'repeat-count': exec_ping.set_repeat,
                'data-size': exec_ping.set_size
                }

            if not vdom:
                paramlist=[]
                for i in params:
                    if params[i]:
                        paramlist.append('execute ping-options {} {}'.format(i,params[i]))
            elif validation.vdomval(self.sshclient,vdom):
                paramlist=['config vdom','edit {}'.format(vdom)]
                for i in params:
                    if params[i]:
                        paramlist.append('execute ping-options {} {}'.format(i,params[i]))

            paramlist.append('execute ping {}'.format(dst))
            try:
                commit(self.sshclient,paramlist)
            except:
                print('Incorrect VDOM/GLOBAL!')

class exec_telnet:

    def __init__(self, sshclient):
        self.sshclient=sshclient

    def set(self, dst, port='', vdom=None):

        if not dst:
            print('PLEASE ENTER A DESTINATION VALUE!')
        else:
            if not vdom:
                paramlist=[]
                paramlist.append('execute telnet {} {}'.format(dst,port))
            elif validation.vdomval(self.sshclient,vdom):
                paramlist=['config vdom','edit {}'.format(vdom)]
                paramlist.append('execute telnet {} {}'.format(dst,port))

            try:
                commit(self.sshclient,paramlist)
            except:
                print('Incorrect VDOM/GLOBAL!')


class exec_ospf_clear:

    def __init__(self, sshclient):
        self.sshclient=sshclient

    def set(self, dst, vdom=None):

        if not vdom:
            paramlist=['execute router clear ospf process']
        elif validation.vdomval(self.sshclient,vdom):
            paramlist=['config vdom','edit {}'.format(vdom),'execute router clear ospf process']

        try:
            return paramlist
        except:
            print('Incorrect VDOM/GLOBAL!')

class auth_list:

    set_source=None
    set_policy=None
    set_user=None
    set_group=None
    set_method=None

    def __init__(self, sshclient):
        self.sshclient=sshclient

    def clear_all():

        auth_list.set_source=None
        auth_list.set_policy=None
        auth_list.set_user=None
        auth_list.set_group=None
        auth_list.set_method=None

    def set(self, vdom=None):

        params= {
            'source': auth_list.set_source,
            'policy': auth_list.set_policy,
            'user': auth_list.set_user,
            'group': auth_list.set_group,
            'method': auth_list.set_method
            }

        if not vdom:
            paramlist=['diagnose firewall auth filter clear']
            for i in params:
                if params[i]:
                    paramlist.append('diagnose firewall auth filter {} {}'.format(i,params[i]))
        elif validation.vdomval(self.sshclient,vdom):
            paramlist=['config vdom','edit {}'.format(vdom),'diagnose firewall auth filter clear']
            for i in params:
                if params[i]:
                    paramlist.append('diagnose firewall auth filter {} {}'.format(i,params[i]))

        paramlist.append('diagnose firewall auth list')
        try:
            commit(self.sshclient,paramlist)
        except:
            print('Incorrect VDOM/GLOBAL!')

class auth_test:

    def __init__(self, sshclient):
        self.sshclient=sshclient

    def set(self, *args, vdom=None, method=None, server_name=None, username=None, password=None):

        if not method or not server_name or not username or not password:
            print('METHOD, SERVER_NAME, USERNAME and PASSWORD have to be filled out!')
        else:
            if not vdom:
                if 'chap' in args or 'pap' in args or 'mschap' in args or 'mschap2' in args:
                    paramlist=['diagnose test authserver {} {} {} {} {}'.format(method, args[0], server_name, username, password)]
                else:
                    paramlist=['diagnose test authserver {} {} {} {}'.format(method, server_name, username, password)]
            elif validation.vdomval(self.sshclient,vdom):
                if 'chap' in args or 'pap' in args or 'mschap' in args or 'mschap2' in args:
                    paramlist=['config vdom','edit {}'.format(vdom),'diagnose test authserver {} {} {} {} {}'.format(method, args[0], server_name, username, password)]
                else:
                    paramlist=['config vdom','edit {}'.format(vdom),'diagnose test authserver {} {} {} {}'.format(method, server_name, username, password)]

        try:
            commit(self.sshclient,paramlist)
        except:
            print('Incorrect VDOM/GLOBAL!')


class exec_sslvpn:

    def __init__(self, sshclient):
        self.sshclient=sshclient

    def set(self, vdom=None):

        if not vdom:
            paramlist=['execute vpn sslvpn list']
        elif validation.vdomval(self.sshclient,vdom):
            paramlist=['config vdom','edit {}'.format(vdom),'execute vpn sslvpn list']

        try:
            commit(self.sshclient,paramlist)
        except:
            print('Incorrect VDOM/GLOBAL!')

class dhcp_list:

    set_interface=None

    def __init__(self, sshclient):
        self.sshclient=sshclient

    def clear_all():

        dhcp_list.set_interface=None

    def set(self, vdom=None,  flt=''):

        if not vdom:
            paramlist=['execute dhcp lease-list {}'.format(flt)]
        elif validation.vdomval(self.sshclient,vdom):
            paramlist=['config vdom','edit {}'.format(vdom),'execute dhcp lease-list {}'.format(flt)]

        try:
            commit(self.sshclient,paramlist)
        except:
            print('Incorrect VDOM/GLOBAL!')


class fmg_device_list:

    def __init__(self, sshclient):
        self.sshclient=sshclient

    def set(self, flt='',option='print'):

        paramlist='diagnose dvm device list {}'.format(flt)

        
        stdout=vdomfunc(self.sshclient,None,None,paramlist)
        return storeprint(stdout,option)
        

class faz_device_list:
    def __init__(self, sshclient):
        self.sshclient=sshclient

    def set(self, flt='list',option='print'):

        paramlist=['diagnose dvm device {}'.format(flt)]

        stdout=vdomfunc(self.sshclient,None,None,paramlist[0])
        return storeprint(stdout,option)


class firewall_iprope:

    def __init__(self, sshclient):
        self.sshclient=sshclient

    def set(self, vdom=None, edit=None, option='print'):

        if not vdom:
            if not edit:
                print('PLEASE ENTER AN EDIT VALUE!')
            else:
                paramlist=['diagnose firewall iprope 100004 {}'.format(edit)]
        elif validation.vdomval(self.sshclient,vdom):
            if not edit:
                print('PLEASE ENTER AN EDIT VALUE!')
            else:
                paramlist=['config vdom','edit {}'.format(vdom),'diagnose firewall iprope show 100004 {}'.format(edit)]

        try:
            return storeprint(self.sshclient,paramlist,option)
        except:
            print('Incorrect VDOM/GLOBAL!')

class exec_dhcp_clear:

    def __init__(self, sshclient):
        self.sshclient=sshclient

    def set(self, vdom=None, flt='all'):

        if not vdom:
            paramlist=['execute dhcp lease-clear {}'.format(flt)]
        elif validation.vdomval(self.sshclient,vdom):
            paramlist=['config vdom','edit {}'.format(vdom),'execute dhcp lease-clear {}'.format(flt)]

        try:
            commit(self.sshclient,paramlist)
        except:
            print('Incorrect VDOM/GLOBAL!')
