from gunslinger import validation

def vdomfunc(sshclient, vdom, precomm, command):
    """To push commands into the FortiGate shell."""
    pushcomm= lambda x: sshclient.exec_command(x)
    if validation.globval(sshclient):
        stdin,stdout,stderr=pushcomm(command)
    elif validation.vdomval(sshclient, vdom)==True or vdom=='global':
        command=precomm+command
        stdin,stdout,stderr=pushcomm(command)

    try:
        return stdout.readlines()
    except:
        print('Incorrect VDOM/GLOBAL!')

def storeprint(stdout, option):
    """To print/store command output from the FortiGate shell."""
    try:
        if option=='print':
            for i in stdout:
                print(i.strip('\n'))
        elif option=='store':
            return stdout
        else:
            print('No available option given!')
    except (UnboundLocalError, TypeError):
        pass


class get:
    """Get commands and subcommands."""
    def __init__(self, sshclient):
        self.sshclient=sshclient

    def sys_ha_status(self, option='print'):
        """Class function to list the information related to the FortiGate's get sys ha status command."""

        precomm="""config global
        """
        command="""get sys ha status
        """

        stdout=vdomfunc(self.sshclient,'global', precomm, command)
        return storeprint(stdout,option)
        
        
    def sys_stat(self, option='print'):
        """Class function to list the information related to the FortiGate's get sys stat command."""

        precomm="""config global
        """
        command="""get sys status
        """

        stdout=vdomfunc(self.sshclient,'global', precomm, command)
        return storeprint(stdout,option)

    def sys_perf_stat(self, option='print'):
        """Class function to list the information related to the FortiGate's get sys perf stat command."""

        precomm="""config global
        """
        command="""get sys perf status
        """

        stdout=vdomfunc(self.sshclient,'global', precomm, command)
        return storeprint(stdout,option)

# Class function to list the information related to the FortiGate's Fortiguard License status.
    def sys_fglic(self, option='print'):
        precomm="""config global
        """
        command="""get sys fortiguard-service status
        """

        stdout=vdomfunc(self.sshclient,'global', precomm, command)
        return storeprint(stdout,option)

    def sys_fortiguard(self, option='print'):
        precomm="""config global
        """
        command="""get sys fortiguard
        """

        stdout=vdomfunc(self.sshclient,'global', precomm, command)
        return storeprint(stdout,option)

    def sys_arp(self, vdom=None, flt='',option='print'):
        precomm="""config vdom
        edit {}
        """.format(vdom)
        command="""get sys arp {}
        """.format(flt)

        stdout=vdomfunc(self.sshclient,vdom,precomm,command)
        return storeprint(stdout,option)


# Class function related to get router info routing-table all.
    def router_monitor(self, vdom=None, flt='all',option='print'):
        precomm="""config vdom
        edit {}
        """.format(vdom)
        command="""get router info routing-table {}
        """.format(flt)

        stdout=vdomfunc(self.sshclient,vdom,precomm,command)
        return storeprint(stdout,option)

    def router_info(self, vdom=None, flt='',option='print'):
        precomm="""config vdom
        edit {}
        """.format(vdom)
        command="""get router info {}
        """.format(flt)

        if not flt:
            print('PLEASE USE A FILTER COMMAND!')
        else:
            stdout=vdomfunc(self.sshclient,vdom,precomm,command)
        return storeprint(stdout,option)

    def router_info_opsf(self, vdom=None, flt='',option='print'):
        print('Options include STATUS, INTERFACE, NEIGHBOR, DATABASE BRIEF and SELF-ORIGINATE, ')
        precomm="""config vdom
        edit {}
        """.format(vdom)
        command="""get router info ospf {}
        """.format(flt)

        stdout=vdomfunc(self.sshclient,vdom,precomm,command)
        return storeprint(stdout,option)

    def router_info_bgp(self, vdom=None, flt='',option='print'):
        precomm="""config vdom
        edit {}
        """.format(vdom)
        command="""get router info bgp {}
        """.format(flt)

        stdout=vdomfunc(self.sshclient,vdom,precomm,command)
        return storeprint(stdout,option)

class get_config:
    def __init__(self, sshclient):
        self.sshclient=sshclient


    def router_static(self, vdom=None, flt=None, option='print'):
        precomm="""config vdom
        edit {}
        """.format(vdom)
        command="""config router static
        edit {}
        get
        """.format(flt)

        stdout=vdomfunc(self.sshclient,vdom,precomm,command)
        return storeprint(stdout,option)

    def firewall_policy(self, vdom=None, flt=None, option='print'):
        precomm="""config vdom
        edit {}
        """.format(vdom)
        command="""config firewall policy
        edit {}
        get
        """.format(flt)

        stdout=vdomfunc(self.sshclient,vdom,precomm,command)
        return storeprint(stdout,option)

   

class show:

    def __init__(self, sshclient):
        self.sshclient=sshclient

    def show_config(self, vdom=None, flt='', option='print'):
        precomm= """config vdom
        edit {}
        """.format(vdom)
        command="""show {}
        """.format(flt)


        if not flt:
            stdout=vdomfunc(self.sshclient,vdom,precomm,command)
        else:
            stdout=vdomfunc(self.sshclient,vdom,precomm,command)
        return storeprint(stdout,option)

    def sys_snmp(self, flt='', option='print'):
        precomm= """config global
        """
        command="""show sys snmp community {}
        """.format(flt)

        stdout=vdomfunc(self.sshclient,'global',precomm,command)
        return storeprint(stdout,option)

    def sys_admin(self, flt='', option='print'):
        precomm= """config global
        """
        command="""show sys admin {}
        """.format(flt)

        stdout=vdomfunc(self.sshclient,'global',precomm,command)
        return storeprint(stdout,option)

# Class function to list the available VDOMs.
    def vdom_props(self, flt='', option='print'):   # vdom=None: the VDOM argument is optional. Proper knowledge of the FortiGate internal workings will be valuable.
        precomm="""config global
        """
        command="""show sys vdom-property {}
        """.format(flt)

        stdout=vdomfunc(self.sshclient,'global', precomm, command)
        return storeprint(stdout,option)

    def sys_int(self, vdom='global', flt='', option='print'):
        precomm1= """config global
        """
        precomm2= """config vdom
        edit {}
        """.format(vdom)
        command="""show sys interface {}
        """.format(flt)

        if vdom=='global':
            stdout=vdomfunc(self.sshclient,vdom,precomm1,command)
        else:
            stdout=vdomfunc(self.sshclient,vdom,precomm2,command)
        return storeprint(stdout,option)

    def router(self, vdom=None, flt='', option='print'):
        precomm="""config vdom
        edit {}
        """.format(vdom)
        command="""show router {}
        """.format(flt)

        stdout=vdomfunc(self.sshclient,vdom,precomm,command)
        return storeprint(stdout, option)

    def firewall_policy(self, vdom=None, flt='', option='print', full=None):
        precomm="""config vdom
        edit {}
        """.format(vdom)
        command="""show {} firewall policy {}
        """
        
        if type(flt) is str:
            command="""show firewall policy {}
            """.format(flt)
    
            if not full:
                stdout=vdomfunc(self.sshclient,vdom,precomm,command.format('',flt))
            elif full==True:
                stdout=vdomfunc(self.sshclient,vdom,precomm,command.format('full',flt))
            
            return storeprint(stdout, option)
        
        elif type(flt) is list:
            listout=[]
            for i in flt:
                command="""show firewall policy {}
                """.format(i)
                #print(i)
                if not full:
                    stdout=vdomfunc(self.sshclient,vdom,precomm,command.format('',flt))
                elif full==True:
                    stdout=vdomfunc(self.sshclient,vdom,precomm,command.format('full',flt))
                
                listout+=stdout
            
            return storeprint(listout, option)

    def firewall_address(self, vdom=None, flt='', option='print', full=None):
        precomm="""config vdom
        edit {}
        """.format(vdom)
        
        if type(flt) is str:
            command="""show firewall address {}
            """.format(flt)
    
            if not full:
                stdout=vdomfunc(self.sshclient,vdom,precomm,command.format('',flt))
            elif full==True:
                stdout=vdomfunc(self.sshclient,vdom,precomm,command.format('full',flt))
            
            return storeprint(stdout, option)
        elif type(flt) is list:
            listout=[]
            for i in flt:
                command="""show firewall address {}
                """.format(i)
                #print(i)
                
                if not full:
                    stdout=vdomfunc(self.sshclient,vdom,precomm,command.format('',flt))
                elif full==True:
                    stdout=vdomfunc(self.sshclient,vdom,precomm,command.format('full',flt))
            
                listout+=stdout
            return storeprint(listout, option)
        
    def firewall_vip(self, vdom=None, flt='', option='print', full=None):
        precomm="""config vdom
        edit {}
        """.format(vdom)
        command="""show firewall vip {}
        """.format(flt)

        if type(flt) is str:
            command="""show firewall vip {}
            """.format(flt)
            
            if not full:
                stdout=vdomfunc(self.sshclient,vdom,precomm,command.format('',flt))
            elif full==True:
                stdout=vdomfunc(self.sshclient,vdom,precomm,command.format('full',flt))
            
            return storeprint(stdout, option)
        elif type(flt) is list:
            listout=[]
            for i in flt:
                command="""show firewall vip {}
                """.format(i)
                #print(i)
                
                if not full:
                    stdout=vdomfunc(self.sshclient,vdom,precomm,command.format('',flt))
                elif full==True:
                    stdout=vdomfunc(self.sshclient,vdom,precomm,command.format('full',flt))
            
                listout+=stdout
            
            return storeprint(listout, option)

    def firewall_group(self, vdom=None, flt='', option='print', full=None):
        precomm="""config vdom
        edit {}
        """.format(vdom)

        if type(flt) is str:
            command="""show firewall addrgrp {}
            """.format(flt)
            
            if not full:
                stdout=vdomfunc(self.sshclient,vdom,precomm,command.format('',flt))
            elif full==True:
                stdout=vdomfunc(self.sshclient,vdom,precomm,command.format('full',flt))
            
            return storeprint(stdout, option)
        elif type(flt) is list:
            listout=[]
            for i in flt:
                command="""show firewall addrgrp {}
                """.format(i)
                #print(i)
                
                if not full:
                    stdout=vdomfunc(self.sshclient,vdom,precomm,command.format('',flt))
                elif full==True:
                    stdout=vdomfunc(self.sshclient,vdom,precomm,command.format('full',flt))
            
                listout+=stdout
            return storeprint(listout, option)

    def user_local(self, vdom=None, flt='', option='print', full=None):
        precomm="""config vdom
        edit {}
        """.format(vdom)
        if type(flt) is str:
            command="""show user local {}
            """.format(flt)
            
            if not full:
                stdout=vdomfunc(self.sshclient,vdom,precomm,command.format('',flt))
            elif full==True:
                stdout=vdomfunc(self.sshclient,vdom,precomm,command.format('full',flt))
            
            return storeprint(stdout, option)
        elif type(flt) is list:
            listout=[]
            for i in flt:
                command="""show user local {}
                """.format(i)
                #print(i)
                
                if not full:
                    stdout=vdomfunc(self.sshclient,vdom,precomm,command.format('',flt))
                elif full==True:
                    stdout=vdomfunc(self.sshclient,vdom,precomm,command.format('full',flt))
            
                listout+=stdout
            return storeprint(listout, option)

    def user_group(self, vdom=None, flt='', option='print', full=None):
        precomm="""config vdom
        edit {}
        """.format(vdom)

        if type(flt) is str:
            command="""show user group {}
            """.format(flt)

            
            if not full:
                stdout=vdomfunc(self.sshclient,vdom,precomm,command.format('',flt))
            elif full==True:
                stdout=vdomfunc(self.sshclient,vdom,precomm,command.format('full',flt))
            
            return storeprint(stdout, option)
        elif type(flt) is list:
            listout=[]
            for i in flt:
                command="""show user group {}
                """.format(i)
                #print(i)
                
                if not full:
                    stdout=vdomfunc(self.sshclient,vdom,precomm,command.format('',flt))
                elif full==True:
                    stdout=vdomfunc(self.sshclient,vdom,precomm,command.format('full',flt))
            
                listout+=stdout
            return storeprint(listout, option)

    def ssl_vpn_settings(self, vdom=None, flt='', option='print'):
        precomm="""config vdom
        edit {}
        """.format(vdom)
        command="""show vpn ssl settings {}
        """.format(flt)

        stdout=vdomfunc(self.sshclient,vdom,precomm,command)
        return storeprint(stdout, option)

    def vpn_phase1(self, vdom=None, flt='', option='print'):
        precomm="""config vdom
        edit {}
        """.format(vdom)
        command="""show vpn ipsec phase1-interface {}
        """.format(flt)

        stdout=vdomfunc(self.sshclient,vdom,precomm,command)
        return storeprint(stdout, option)

    def vpn_phase2(self, vdom=None, flt='', option='print'):
        precomm="""config vdom
        edit {}
        """.format(vdom)
        command="""show vpn ipsec phase2-interface {}
        """.format(flt)

        stdout=vdomfunc(self.sshclient,vdom,precomm,command)
        return storeprint(stdout, option)
