class ReadableRate():
    def __init__(self,x):
        num = len(str(x))
        if num < 4:
            self.rate = str(x) + " b"
        elif num < 7:
            x = x / 1000.0
            self.rate = str("%.1f" + " K") % x
        elif num < 10:
            x = x / 1000000.0
            self.rate = str("%.1f" + " M") % x
        else:
            x = x / 1000000000.0
            self.rate = str("%.1f" + " G") % x

def get_host():
    import sys
    from getpass import getpass
    JUNIPER = ['junos','juniper']
    CISCO_IOS = ['cisco','cisco_ios','ios','cisco-ios','cisco ios']
    CISCO_XR = ['xr','cisco_xr','cisco-xr','ios-xr','ios xr']
    
    rtr = raw_input('Hostname/IP:')
    os = raw_input('Device OS: ')
    username = raw_input('Username:')
    password = getpass()
    
    os = os.lower()
    if os in JUNIPER:
        os = 'juniper'
    elif os in CISCO_IOS:
        os = 'cisco_ios'
    elif os in CISCO_XR:
        os = 'cisco_xr'
    else:
        print 'ERR: OS should be juniper, ios or xr'
        sys.exit()
    
    host = {
        'device_type': os,
        'ip' : rtr,
        'username' : username,
        'password': password,
        'port': 22,
        'ssh_config_file': '~/.ssh/proxy.config',
        'verbose': False,
    }
    return host