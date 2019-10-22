import paramiko
import re

def globval(sshclient):
    command="""config global
    """
    stdin,stdout,stderr=sshclient.exec_command(command)
    for i in stdout.readlines():
        if re.match(r'(Command fail. Return code 1)',i, flags=0):
            return True


def vdomval(sshclient, vdom):
    precomm="""config global
    """
    command="""show sys vdom-property
    """

    stdin,stdout,stderr=sshclient.exec_command(precomm+command)

    if vdom==None:
            print('Please specify a VDOM!')
    else:
        for i in stdout.readlines():
            if re.match(r'.+(edit \"'+vdom+'\")',i, flags=0):
                return True

def adminval(sshclient, name):
    precomm="""config global
    """
    command="""show sys admin
    """

    if globval(sshclient):
        stdin,stdout,stderr=sshclient.exec_command(command)
    else:
        stdin,stdout,stderr=sshclient.exec_command(precomm+command)

    if name==None:
            print('Please specify a ADMIN USER!')
    else:
        for i in stdout.readlines():
            if re.match(r'.+(edit \"'+name+'\")',i, flags=0):
                return True

def intval(sshclient, name):
    precomm="""config global
    """
    command="""show sys interface {}
    """.format(name)

    if globval(sshclient):
        stdin,stdout,stderr=sshclient.exec_command(command)
    else:
        stdin,stdout,stderr=sshclient.exec_command(precomm+command)

    if name==None:
        print('Please specify an interface name!')
    else:
        for i in stdout.readlines():
            if re.match(r'.+(edit \"'+name+'\")',i, flags=0):
                return True

def policyval(sshclient, vdom, edit):
    precomm="""config vdom
    edit {}
    """.format(vdom)
    command="""show firewall policy
    """

    if not vdomval(sshclient,vdom):
        stdin,stdout,stderr=sshclient.exec_command(command)
    else:
        stdin,stdout,stderr=sshclient.exec_command(precomm+command)

    if edit==None:
        print('Please specify an address name!')
    for i in stdout.readlines():
        if re.match(r'.+(edit \"'+edit+'\")',i, flags=0):
            return True

def addrval(sshclient, vdom, name):
    precomm="""config vdom
    edit {}
    """.format(vdom)
    command="""show firewall address
    """

    if not vdomval(sshclient,vdom):
        stdin,stdout,stderr=sshclient.exec_command(command)
    else:
        stdin,stdout,stderr=sshclient.exec_command(precomm+command)

    if name==None:
        print('Please specify an address name!')
    for i in stdout.readlines():
        if re.match(r'.+(edit \"'+name+'\")',i, flags=0):
            return True

def addrgrpval(sshclient, vdom, name):
    precomm="""config vdom
    edit {}
    """.format(vdom)
    command="""show firewall addrgrp
    """

    if not vdomval(sshclient,vdom):
        stdin,stdout,stderr=sshclient.exec_command(command)
    else:
        stdin,stdout,stderr=sshclient.exec_command(precomm+command)

    if name==None:
        print('Please specify an address name!')
    for i in stdout.readlines():
        if re.match(r'.+(edit \"'+name+'\")',i, flags=0):
            return True

def srvval(sshclient, vdom, name):
    precomm="""config vdom
    edit {}
    """.format(vdom)
    command="""show firewall service
    """

    if not vdomval(sshclient,vdom):
        stdin,stdout,stderr=sshclient.exec_command(command)
    else:
        stdin,stdout,stderr=sshclient.exec_command(precomm+command)

    if name==None:
        print('Please specify an service name!')
    for i in stdout.readlines():
        if re.match(r'.+(edit \"'+name+'\")',i, flags=0):
            return True

def phase1val(sshclient, vdom, name):
    precomm="""config vdom
    edit {}
    """.format(vdom)
    command="""show vpn ipsec phase1-interface
    """

    if not vdomval(sshclient,vdom):
        stdin,stdout,stderr=sshclient.exec_command(command)
    else:
        stdin,stdout,stderr=sshclient.exec_command(precomm+command)

    if name==None:
        print('Please specify a Phase1 name!')
    for i in stdout.readlines():
        if re.match(r'.+(edit \"'+name+'\")',i, flags=0):
            return True

def phase2val(sshclient, vdom, name):
    precomm="""config vdom
    edit {}
    """.format(vdom)
    command="""show vpn ipsec phase2-interface
    """

    if not vdomval(sshclient,vdom):
        stdin,stdout,stderr=sshclient.exec_command(command)
    else:
        stdin,stdout,stderr=sshclient.exec_command(precomm+command)

    if name==None:
        print('Please specify a Phase2 name!')
    for i in stdout.readlines():
        if re.match(r'.+(edit \"'+name+'\")',i, flags=0):
            return True
