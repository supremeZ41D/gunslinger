import paramiko

# It returns an SSHClient Paramiko object.
def access(ip, port=22, username=None, password=None):
    sshclient= paramiko.SSHClient()
    sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        sshclient.connect(ip, port=str(port), username=username, password=password)
    except TimeoutError:
        print('ERROR WHILE ATTEMPTING TO LOG IN!')
    return sshclient

# Session closure. Please be aware of closing the session while storing said result into your sshclient variable, for example, sshclient= close(sshclient)
def close(sshclient):
    sshclient.close()  
# Session closure. Please be aware of closing the session while storing said result into your sshclient variable, for example, sshclient= close(sshclient)