from gunslinger import validation

def fwscript(sshclient, path='C:/Users/omar.brito/Documents/Python_Security_Exercises/Plantilla SOC 17-10-2018.txt'):
    txfile=open(path,'r')
    txlist=txfile.readlines()
    stdin,stdout,stderr=sshclient.exec_command(''.join(txlist))
    print('SCRIPT PUSHED!')
    txfile.close()

def commit(sshclient, paramlist):
    stdin,stdout,stderr=sshclient.exec_command('\n'.join(paramlist)+'\nend\nend\n')
    #print(stdout.readlines())
    print('SCRIPT PUSHED!')

def paramfunc(params, paramlist, action):
    if action=='set':
        for i in params:
            if params[i]:
                paramlist.append('set {} {}'.format(i,params[i]))
    elif action=='unset':
        for i in params:
            if params[i]:
                paramlist.append('unset {} {}'.format(i,params[i]))
    elif action=='append':
        for i in params:
            if i=='member' and params[i]:
                paramlist.append('append member {}'.format(params[i]))
    elif action=='unselect' and params[i]:
        for i in params:
            if i=='member':
                paramlist.append('unselect member {}'.format(params[i]))

    return paramlist

class snmp_community:

    """Configure the SNMP community."""
    set_edit=None
    set_name= None
    set_events= None
    set_host_entry= None
    set_host= None

    def __init__(self, sshclient):
        self.sshclient=sshclient

    def clear_all():

        snmp_community.set_name= None
        snmp_community.set_events= None
        snmp_community.set_edit= None
        snmp_community.set_host_entry= None
        snmp_community.set_host= None

    def preview(self, action='set', option='edit'):

        params= {
                'name': snmp_community.set_name,
                'event': snmp_community.set_events
                }

        if option=='edit':
            if validation.globval(self.sshclient):
                paramlist=['config sys snmp community','{} {}'.format(option,snmp_community.set_edit)]
                if snmp_community.set_edit=='0':
                    print('A new SNMP community will be created once committed.')
                    paramlist=paramfunc(params, paramlist, action)
                else:
                    paramlist=paramfunc(params, paramlist, action)
            else:
                paramlist=['config global','config sys snmp community','{} {}'.format(option,snmp_community.set_edit)]
                if snmp_community.set_edit=='0':
                    print('A new SNMP community will be created once committed.')
                    paramlist=paramfunc(params, paramlist, action)
                else:
                    paramlist=paramfunc(params, paramlist, action)


        elif option=='delete':
            if validation.globval(self.sshclient):
                paramlist=['config sys snmp community','{} {}'.format(option,snmp_community.set_edit)]
                paramlist=paramfunc(params, paramlist, action)
            else:
                paramlist=['config global','config sys snmp community','{} {}'.format(option,snmp_community.set_edit)]
                paramlist=paramfunc(params, paramlist, action)

        if snmp_community.hosts(snmp_community.set_host,action,snmp_community.set_host_entry):
            paramlist+=snmp_community.hosts(snmp_community.set_host,action,snmp_community.set_host_entry)

        try:
            return paramlist
        except:
            print('SOME PARAMETER(S) NOT FOUND!')

    def hosts(host, action, entry):

        if not entry or not host:
            return None
        else:
            hostparam=['config hosts','edit {}'.format(entry),'{} ip {} 255.255.255.255'.format(action,host),'next','end']
            return hostparam

class snmp_sysinfo:

    set_trap_lowRAM_threshold= None

    def __init__(self, sshclient):
        self.sshclient=sshclient

    def clear_all():

        snmp_sysinfo.set_trap_lowRAM_threshold= None

    def set(self, action='set'):

        params= {
                'trap-low-memory-threshold': snmp_sysinfo.set_trap_lowRAM_threshold
                }

        if validation.globval(self.sshclient):
            paramlist=['config sys snmp sysinfo']
            paramlist=paramfunc(params, paramlist, action)
        else:
            paramlist=['config global','config sys snmp sysinfo']
            paramlist=paramfunc(params, paramlist, action)

        try:
            return paramlist
        except:
            print('SOME PARAMETER(S) NOT FOUND!')


class router_static:

    set_status='enable'
    set_edit=None
    set_dst=None
    set_gateway=None
    set_device=None
    set_distance=None
    set_priority=None

    def __init__(self, sshclient):
        self.sshclient=sshclient

    def clear_all():

        router_static.set_status=None
        router_static.set_edit=None
        router_static.set_dst=None
        router_static.set_gateway=None
        router_static.set_device=None
        router_static.set_distance=None
        router_static.set_priority=None

    def preview(self, action='set', vdom=None, option='edit'):

        if not router_static.set_edit:
            print('PLEASE ENTER AN EDIT VALUE!')
        else:
            params= {
                'status': router_static.set_status,
                'dst': router_static.set_dst,
                'gateway': router_static.set_gateway,
                'device': router_static.set_device,
                'distance': router_static.set_distance,
                'priority': router_static.set_priority
                }

            if option=='edit':
                if not vdom:
                    paramlist=['config router static','{} {}'.format(option,router_static.set_edit)]
                    if router_static.set_edit=='0':
                        print('A new static route will be created once committed.')
                        if validation.intval(self.sshclient,router_static.set_device):
                            paramlist=paramfunc(params, paramlist, action)
                    else:
                        paramlist=paramfunc(params, paramlist, action)
                elif validation.vdomval(self.sshclient,vdom):
                    paramlist=['config vdom','edit {}'.format(vdom),'config router static','{} {}'.format(option,router_static.set_edit)]
                    if router_static.set_edit=='0':
                        print('A new static route will be created once committed.')
                        if validation.intval(self.sshclient,router_static.set_device):
                            paramlist=paramfunc(params, paramlist, action)
                    else:
                        paramlist=paramfunc(params, paramlist, action)

            elif option=='delete':
                if not vdom:
                    paramlist=['config router static','{} {}'.format(option,router_static.set_edit)]
                    paramlist=paramfunc(params, paramlist, action)
                elif validation.vdomval(self.sshclient,vdom):
                    paramlist=['config vdom','edit {}'.format(vdom),'config router static','{} {}'.format(option,router_static.set_edit)]
                    paramlist=paramfunc(params, paramlist, action)

            print('*** NOTE: For deployment, the minimum requirements are to have STATUS, DST, GATEWAY an DEVICE with values! ***')
            try:
                return paramlist
            except:
                print('SOME PARAMETER(S) NOT FOUND!')

class firewall_address:

    set_name=None
    set_type=None
    set_fqdn=None
    set_subnet=None
    set_route=None
    set_comment=None

    def __init__(self, sshclient):
        self.sshclient=sshclient

    def clear_all():

        firewall_address.set_comment=None
        firewall_address.set_name=None
        firewall_address.set_type=None
        firewall_address.set_fqdn=None
        firewall_address.set_subnet=None
        firewall_address.set_route=None

    def preview(self, action='set', vdom=None, option='edit'):
        if not firewall_address.set_name:
            print('PLEASE ENTER AN NAME VALUE!')
        else:
            params= {
                'type': firewall_address.set_type,
                'fqdn': firewall_address.set_fqdn,
                'subnet': firewall_address.set_subnet,
                'route': firewall_address.set_route,
                'comment': firewall_address.set_comment
                }

            if option=='edit':
                if not vdom:
                    paramlist=['config firewall address','{} {}'.format(option,firewall_address.set_name)]
                    if not validation.addrval(self.sshclient,vdom,firewall_address.set_name):
                        print('Address {} will be created once committed.'.format(firewall_address.set_name))
                        paramlist=paramfunc(params, paramlist, action)
                    else:
                        paramlist=paramfunc(params, paramlist, action)
                elif validation.vdomval(self.sshclient,vdom):
                    paramlist=['config vdom','edit {}'.format(vdom),'config firewall address','{} {}'.format(option,firewall_address.set_name)]
                    if not validation.addrval(self.sshclient,vdom,firewall_address.set_name):
                        print('Address {} will be created once committed.'.format(firewall_address.set_name))
                        paramlist=paramfunc(params, paramlist, action)
                    else:
                        paramlist=paramfunc(params, paramlist, action)

            elif option=='delete':
                if not vdom:
                    paramlist=['config firewall address','{} {}'.format(option,firewall_address.set_name)]
                    paramlist=paramfunc(params, paramlist, action)
                elif validation.vdomval(self.sshclient,vdom):
                    paramlist=['config vdom','edit {}'.format(vdom),'config firewall address','{} {}'.format(option,firewall_address.set_name)]
                    paramlist=paramfunc(params, paramlist, action)

            try:
                return paramlist
            except:
                print('SOME PARAMETER(S) NOT FOUND!')

class firewall_addrgrp:

    set_name=None
    set_member=None
    set_comment=None

    def __init__(self, sshclient):
        self.sshclient=sshclient

    def clear_all():

        firewall_addrgrp.set_name=None
        firewall_addrgrp.set_member=None
        firewall_addrgrp.set_comment=None

    def preview(self, action='set', vdom=None, option='edit'):
        if not firewall_address.set_name:
            print('PLEASE ENTER AN NAME VALUE!')
        else:
            params= {
                'member': firewall_addrgrp.set_member,
                'comment': firewall_addrgrp.set_comment
                }

            if option=='edit':
                if not vdom:
                    paramlist=['config firewall addrgrp','{} {}'.format(option,firewall_addrgrp.set_name)]
                    if not validation.addrgrpval(self.sshclient,vdom,firewall_addrgrp.set_name):
                        print('Address group {} will be created once committed.'.format(firewall_addrgrp.set_name))
                        paramlist=paramfunc(params, paramlist, action)
                    else:
                        paramlist=paramfunc(params, paramlist, action)
                elif validation.vdomval(self.sshclient,vdom):
                    paramlist=['config vdom','edit {}'.format(vdom),'config firewall addrgrp','{} {}'.format(option,firewall_addrgrp.set_name)]
                    if not validation.addrgrpval(self.sshclient,vdom,firewall_addrgrp.set_name):
                        print('Address group {} will be created once committed.'.format(firewall_addrgrp.set_name))
                        paramlist=paramfunc(params, paramlist, action)
                    else:
                        paramlist=paramfunc(params, paramlist, action)

            elif option=='delete':
                if not vdom:
                    paramlist=['config firewall addrgrp','{} {}'.format(option,firewall_addrgrp.set_name)]
                    paramlist=paramfunc(params, paramlist, action)
                elif validation.vdomval(self.sshclient,vdom):
                    paramlist=['config vdom','edit {}'.format(vdom),'config firewall addrgrp','{} {}'.format(option,firewall_addrgrp.set_name)]
                    paramlist=paramfunc(params, paramlist, action)

            try:
                return paramlist
            except:
                print('SOME PARAMETER(S) NOT FOUND!')

class firewall_service:

    set_name=None
    set_tcp_port_range=None
    set_udp_port_range=None
    set_comment=None

    def __init__(self, sshclient):
        self.sshclient=sshclient

    def clear_all():

        firewall_service.set_name=None
        firewall_service.set_tcp_port_range=None
        firewall_service.set_udp_port_range=None
        firewall_service.set_comment=None

    def preview(self, action='set', vdom=None, option='edit'):
        if not firewall_service.set_name:
            print('PLEASE ENTER AN NAME VALUE!')
        else:
            params= {
                'tcp-portrange': firewall_service.set_tcp_port_range,
                'udp-portrange': firewall_service.set_udp_port_range,
                'comment': firewall_addrgrp.set_comment
                }

            if option=='edit':
                if not vdom:
                    paramlist=['config firewall service custom','{} {}'.format(option,firewall_service.set_name)]
                    if not validation.addrgrpval(self.sshclient,vdom,firewall_service.set_name):
                        print('Address group {} will be created once committed.'.format(firewall_service.set_name))
                        paramlist=paramfunc(params, paramlist, action)
                    else:
                        paramlist=paramfunc(params, paramlist, action)
                elif validation.vdomval(self.sshclient,vdom):
                    paramlist=['config vdom','edit {}'.format(vdom),'config firewall service custom','{} {}'.format(option,firewall_service.set_name)]
                    if not validation.addrgrpval(self.sshclient,vdom,firewall_service.set_name):
                        print('Address group {} will be created once committed.'.format(firewall_service.set_name))
                        paramlist=paramfunc(params, paramlist, action)
                    else:
                        paramlist=paramfunc(params, paramlist, action)

            elif option=='delete':
                if not vdom:
                    paramlist=['config firewall service custom','{} {}'.format(option,firewall_service.set_name)]
                    paramlist=paramfunc(params, paramlist, action)
                elif validation.vdomval(self.sshclient,vdom):
                    paramlist=['config vdom','edit {}'.format(vdom),'config firewall service custom','{} {}'.format(option,firewall_service.set_name)]
                    paramlist=paramfunc(params, paramlist, action)

            try:
                return paramlist
            except:
                print('SOME PARAMETER(S) NOT FOUND!')

class sys_int:

    set_name=None
    set_vdom=None
    set_vlanid=None
    set_interface=None
    set_ip=None
    set_allowaccess=None
    set_description=None
    set_alias=None
    set_snmp=None
    set_status=None
    set_comment=None

    def __init__(self, sshclient):
        self.sshclient=sshclient

    def clear_all():

        sys_int.set_name=None
        sys_int.set_vdom=None
        sys_int.set_vlanid=None
        sys_int.set_interface=None
        sys_int.set_ip=None
        sys_int.set_allowaccess=None
        sys_int.set_description=None
        sys_int.set_alias=None
        sys_int.set_snmp=None
        sys_int.set_status=None
        sys_int.set_comment=None

    def preview(self, action='set', vdom=None, option='edit'):

        if not sys_int.set_name:
            print('PLEASE ENTER AN NAME VALUE!')
        else:
            params= {
                'vdom': sys_int.set_vdom,
                'vlanid': sys_int.set_vlanid,
                'interface': sys_int.set_interface,
                'ip': sys_int.set_ip,
                'allowaccess': sys_int.set_allowaccess,
                'description': sys_int.set_description,
                'alias': sys_int.set_alias,
                'snmp-index': sys_int.set_snmp,
                'status': sys_int.set_status,
                'comment': sys_int.set_comment
                }

            if option=='edit':
                if not vdom:
                    paramlist=['config system interface','{} {}'.format(option,sys_int.set_name)]
                    if not validation.intval(self.sshclient,vdom,sys_int.set_name):
                        print('Interface {} will be created once committed.'.format(sys_int.set_name))
                        paramlist=paramfunc(params, paramlist, action)
                    else:
                        paramlist=paramfunc(params, paramlist, action)
                elif validation.vdomval(self.sshclient,vdom):
                    paramlist=['config vdom','edit {}'.format(vdom),'config system interface','{} {}'.format(option,sys_int.set_name)]
                    if not validation.intval(self.sshclient,vdom,sys_int.set_name):
                        print('Interface {} will be created once committed.'.format(sys_int.set_name))
                        paramlist=paramfunc(params, paramlist, action)
                    else:
                        paramlist=paramfunc(params, paramlist, action)

            elif option=='delete':
                if not vdom:
                    paramlist=['config system interface','{} {}'.format(option,sys_int.set_name)]
                    paramlist=paramfunc(params, paramlist, action)
                elif validation.vdomval(self.sshclient,vdom):
                    paramlist=['config vdom','edit {}'.format(vdom),'config system interface','{} {}'.format(option,sys_int.set_name)]
                    paramlist=paramfunc(params, paramlist, action)

            try:
                return paramlist
            except:
                print('SOME PARAMETER(S) NOT FOUND!')

class firewall_policy:

    set_edit=None
    set_srcintf=None
    set_dstintf=None
    set_srcaddr=None
    set_dstaddr=None
    set_action=None
    set_schedule=None
    set_service=None
    set_logtraffic=None
    set_comment=None
    set_nat=None
    set_fsso=None
    set_ntlm=None
    set_status=None

    def __init__(self, sshclient):
        self.sshclient=sshclient

    def clear_all():

        firewall_policy.set_edit=None
        firewall_policy.set_srcintf=None
        firewall_policy.set_dstintf=None
        firewall_policy.set_srcaddr=None
        firewall_policy.set_dstaddr=None
        firewall_policy.set_action=None
        firewall_policy.set_schedule=None
        firewall_policy.set_service=None
        firewall_policy.set_logtraffic=None
        firewall_policy.set_comment=None
        firewall_policy.set_nat=None
        firewall_policy.set_ntlm=None
        firewall_policy.set_fsso=None
        firewall_policy.set_status=None


    def preview(self, action='set', vdom=None, option='edit'):

        if not firewall_policy.set_edit:
            print('PLEASE ENTER AN EDIT VALUE!')
        else:
            params= {
                'srcintf': firewall_policy.set_srcintf,
                'dstintf': firewall_policy.set_dstintf,
                'srcaddr': firewall_policy.set_srcaddr,
                'dstaddr': firewall_policy.set_dstaddr,
                'action': firewall_policy.set_action,
                'schedule': firewall_policy.set_schedule,
                'service': firewall_policy.set_service,
                'logtraffic': firewall_policy.set_logtraffic,
                'comment': firewall_policy.set_comment,
                'nat': firewall_policy.set_nat,
                'ntlm': firewall_policy.set_ntlm,
                'fsso': firewall_policy.set_fsso,
                'status': firewall_policy.set_status
                }

            if option=='edit':
                if not vdom:
                    paramlist=['config firewall policy','{} {}'.format(option,firewall_policy.set_edit)]
                    if firewall_policy.set_edit=='0':
                        print('A new policy will be created once committed.')
                        if validation.intval(self.sshclient,vdom,firewall_policy.set_srcintf) and validation.intval(self.sshclient,vdom,firewall_policy.set_dstintf) and validation.addrval(self.sshclient,vdom,firewall_policy.set_srcaddr) and validation.addrval(self.sshclient,vdom,firewall_policy.set_dstaddr) and validation.srvval(self.sshclient,vdom,firewall_policy.set_service):
                            paramlist=paramfunc(params, paramlist, action)
                    else:
                        paramlist=paramfunc(params, paramlist, action)
                elif validation.vdomval(self.sshclient,vdom):
                    paramlist=['config vdom','edit {}'.format(vdom),'config firewall policy','{} {}'.format(option,firewall_policy.set_edit)]
                    if firewall_policy.set_edit=='0':
                        print('A new policy will be created once committed.')
                        if validation.intval(self.sshclient,vdom,firewall_policy.set_srcintf) and validation.intval(self.sshclient,vdom,firewall_policy.set_dstintf) and validation.addrval(self.sshclient,vdom,firewall_policy.set_srcaddr) and validation.addrval(self.sshclient,vdom,firewall_policy.set_dstaddr) and validation.srvval(self.sshclient,vdom,firewall_policy.set_service):
                            paramlist=paramfunc(params, paramlist, action)
                    else:
                        paramlist=paramfunc(params, paramlist, action)

            elif option=='delete':
                if not vdom:
                    paramlist=['config firewall policy','{} {}'.format(option,firewall_policy.set_edit)]
                    paramlist=paramfunc(params, paramlist, action)
                elif validation.vdomval(self.sshclient,vdom):
                    paramlist=['config vdom','edit {}'.format(vdom),'config firewall policy','{} {}'.format(option,firewall_policy.set_edit)]
                    paramlist=paramfunc(params, paramlist, action)

            try:
                return paramlist
            except:
                print('SOME PARAMETER(S) NOT FOUND!')

class admin_user:

    set_accprofile=None
    set_vdom=None
    set_password=None

    def __init__(self, sshclient):
        self.sshclient=sshclient

    def clear_all():

        admin_user.set_name=None
        admin_user.set_accprofile=None
        admin_user.set_vdom=None
        admin_user.set_password=None

    def preview(self, action='set', option='edit'):

        if not option:
            print('Please enter \"edit\" or \"delete\"!')
        else:
            params= {
                'accprofile': admin_user.set_accprofile,
                'vdom': admin_user.set_vdom,
                'password': admin_user.set_password
                }

            if option=='edit':
                if validation.globval(self.sshclient):
                    paramlist=['config sys admin','{} {}'.format(option,admin_user.set_name)]
                    if not validation.adminval(self.sshclient,admin_user.set_name):
                        print('A new admin username will be created once committed.')
                        paramlist=paramfunc(params, paramlist, action)
                    else:
                        paramlist=paramfunc(params, paramlist, action)
                else:
                    paramlist=['config global','config sys admin','{} {}'.format(option,admin_user.set_name)]
                    if not validation.adminval(self.sshclient,admin_user.set_name):
                        print('A new admin username will be created once committed.')
                        paramlist=paramfunc(params, paramlist, action)
                    else:
                        paramlist=paramfunc(params, paramlist, action)

            elif option=='delete':
                if validation.globval(self.sshclient):
                    paramlist=['config sys admin','{} {}'.format(option,admin_user.set_name)]
                    paramlist=paramfunc(params, paramlist, action)
                else:
                    paramlist=['config global','config sys admin','{} {}'.format(option,admin_user.set_name)]
                    paramlist=paramfunc(params, paramlist, action)

            try:
                return paramlist
            except:
                print('SOME PARAMETER(S) NOT FOUND!')


class vpn_phase1:

    set_name=None
    set_interface=None
    set_ike=None
    set_keylife=None
    set_peertype=None
    set_proposal=None
    set_dpd=None
    set_dhgrp=None
    set_natt=None
    set_gw=None
    set_psk=None
    set_dpdretry=None
    set_comment=None


    def __init__(self, sshclient):
        self.sshclient=sshclient

    def clear_all():

        vpn_phase1.set_name=None
        vpn_phase1.set_interface=None
        vpn_phase1.set_ike=None
        vpn_phase1.set_keylife=None
        vpn_phase1.set_peertype=None
        vpn_phase1.set_proposal=None
        vpn_phase1.set_dpd=None
        vpn_phase1.set_dhgrp=None
        vpn_phase1.set_natt=None
        vpn_phase1.set_gw=None
        vpn_phase1.set_psk=None
        vpn_phase1.set_dpdretry=None
        vpn_phase1.set_comment=None

    def preview(self, action='set', vdom=None, option='edit'):

        if not vpn_phase1.set_name:
            print('PLEASE ENTER AN EDIT VALUE!')
        else:
            params= {
                'interface': vpn_phase1.set_interface,
                'ike-version': vpn_phase1.set_ike,
                'keylife': vpn_phase1.set_keylife,
                'peertype': vpn_phase1.set_peertype,
                'proposal': vpn_phase1.set_proposal,
                'dpd': vpn_phase1.set_dpd,
                'dhgrp': vpn_phase1.set_dhgrp,
                'nattraversal': vpn_phase1.set_natt,
                'remote-gw': vpn_phase1.set_gw,
                'psksecret': vpn_phase1.set_psk,
                'dpd-retryinterval': vpn_phase1.set_dpdretry,
                'comment': vpn_phase1.set_comment
                }

            if option=='edit':
                if not vdom:
                    paramlist=['config vpn ipsec phase1-interface','{} {}'.format(option,vpn_phase1.set_name)]
                    if not validation.phase1val(self.sshclient,vdom,vpn_phase1.set_name):
                        print('Phase1 {} will be created once committed.'.format(vpn_phase1.set_name))
                        if validation.intval(self.sshclient,vdom,vpn_phase1.set_interface):
                            paramlist=paramfunc(params, paramlist, action)
                    else:
                        paramlist=paramfunc(params, paramlist, action)
                elif validation.vdomval(self.sshclient,vdom):
                    paramlist=['config vdom','edit {}'.format(vdom),'config vpn ipsec phase1-interface','{} {}'.format(option,vpn_phase1.set_name)]
                    if not validation.phase1val(self.sshclient,vdom,vpn_phase1.set_name):
                        print('Phase1 {} will be created once committed.'.format(vpn_phase1.set_name))
                        if validation.intval(self.sshclient,vdom,vpn_phase1.set_interface):
                            paramlist=paramfunc(params, paramlist, action)
                    else:
                        paramlist=paramfunc(params, paramlist, action)

            elif option=='delete':
                if not vdom:
                    paramlist=['config vpn ipsec phase1-interface','{} {}'.format(option,vpn_phase1.set_name)]
                    paramlist=paramfunc(params, paramlist, action)
                elif validation.vdomval(self.sshclient,vdom):
                    paramlist=['config vdom','edit {}'.format(vdom),'config vpn ipsec phase1-interface','{} {}'.format(option,vpn_phase1.set_name)]
                    paramlist=paramfunc(params, paramlist, action)

            try:
                return paramlist
            except:
                print('SOME PARAMETER(S) NOT FOUND!')

class vpn_phase2:

    set_name=None
    set_phase1=None
    set_proposal=None
    set_dhgrp=None
    set_keylife=None
    set_localdom=None
    set_remotedom=None
    set_comment=None

    def __init__(self, sshclient):
        self.sshclient=sshclient

    def clear_all():

        vpn_phase2.set_name=None
        vpn_phase2.set_phase1=None
        vpn_phase2.set_proposal=None
        vpn_phase2.set_dhgrp=None
        vpn_phase2.set_keylife=None
        vpn_phase2.set_localdom=None
        vpn_phase2.set_remotedom=None
        vpn_phase2.set_comment=None

    def preview(self, action='set', vdom=None, option='edit'):

        if not vpn_phase2.set_name:
            print('PLEASE ENTER AN EDIT VALUE!')
        else:
            params= {
                'phase1name': vpn_phase2.set_phase1,
                'proposal': vpn_phase2.set_proposal,
                'dhgrp': vpn_phase2.set_dhgrp,
                'keylifeseconds': vpn_phase2.set_keylife,
                'src-subnet': vpn_phase2.set_localdom,
                'dst-subnet': vpn_phase2.set_remotedom,
                'comment': vpn_phase2.set_comment
                }

            if option=='edit':
                if not vdom:
                    paramlist=['config vpn ipsec phase2-interface','{} {}'.format(option,vpn_phase2.set_name)]
                    if not validation.phase2val(self.sshclient,vdom,vpn_phase2.set_name):
                        print('Phase2 {} will be created once committed.'.format(vpn_phase2.set_name))
                        if validation.phase1val(self.sshclient,vdom,vpn_phase2.set_phase1):
                            paramlist=paramfunc(params, paramlist, action)
                    else:
                        paramlist=paramfunc(params, paramlist, action)
                elif validation.vdomval(self.sshclient,vdom):
                    paramlist=['config vdom','edit {}'.format(vdom),'config vpn ipsec phase2-interface','{} {}'.format(option,vpn_phase2.set_name)]
                    if not validation.phase2val(self.sshclient,vdom,vpn_phase2.set_name):
                        print('Phase2 {} will be created once committed.'.format(vpn_phase2.set_name))
                        if validation.phase1val(self.sshclient,vdom,vpn_phase2.set_phase1):
                            paramlist=paramfunc(params, paramlist, action)
                    else:
                        paramlist=paramfunc(params, paramlist, action)
            elif option=='delete':
                if not vdom:
                    paramlist=['config vpn ipsec phase2-interface','{} {}'.format(option,vpn_phase2.set_name)]
                    paramlist=paramfunc(params, paramlist, action)
                elif validation.vdomval(self.sshclient,vdom):
                    paramlist=['config vdom','edit {}'.format(vdom),'config vpn ipsec phase2-interface','{} {}'.format(option,vpn_phase2.set_name)]
                    paramlist=paramfunc(params, paramlist, action)
            try:
                return paramlist
            except:
                print('SOME PARAMETER(S) NOT FOUND!')
