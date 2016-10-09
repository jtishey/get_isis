#-------------------------------------------#
# Converts rate to bits, Kb, Mb, or Gb      |
#-------------------------------------------#

class ReadableRate():
    def __init__(self,x):
        num = len(str(x))
        if num < 4:                                # < 4 digits = bits
            self.rate = str(x) + " b"
        elif num < 7:                              # < 7 digits = Kilobits
            x = x / 1000.0
            self.rate = str("%.1f" + " K") % x
        elif num < 10:                             # < 10 digits = Megabits
            x = x / 1000000.0
            self.rate = str("%.1f" + " M") % x
        else:
            x = x / 1000000000.0                   # 10+ digits = Gigabits
            self.rate = str("%.1f" + " G") % x


#-------------------------------------------#
# Get host/IP, user, pass, and device type  #
#-------------------------------------------#
def get_host():
    import sys
    from getpass import getpass

    # Things that can be entered to define OS:
    JUNIPER = ['junos', 'juniper', 'j', 'jun']
    CISCO_IOS = ['cisco', 'cisco_ios', 'ios', 'cisco-ios', 'cisco ios', 'i']
    CISCO_XR = ['xr', 'cisco_xr', 'cisco-xr', 'ios-xr', 'ios xr', 'x']

    # Grab info:
    rtr = raw_input('Hostname/IP:')
    os = raw_input('Device OS:').lower()
    while os not in JUNIPER and os not in CISCO_IOS and os not in CISCO_XR:
        print 'ERR: Please enter junos, ios, or xr'
        os = raw_input('Device OS:').lower()
    username = raw_input('Username:')
    password = getpass()
    proxy = raw_input('Use .ssh/proxy.config? [y/n]:').lower()
    while proxy != 'y' and proxy != 'n':
        print 'ERR: Please enter y/n for proxy'
        proxy = raw_input('Use .ssh/proxy.config? [y/n]:').lower()

    # Correct user input:
    os = os.lower()
    if os in JUNIPER:
        os = 'juniper'
    elif os in CISCO_IOS:
        os = 'cisco_ios'
    elif os in CISCO_XR:
        os = 'cisco_xr'

    # Define host dict for netmiko:
    host = {
        'device_type': os,
        'ip': rtr,
        'username': username,
        'password': password,
        'port': 22,
        'verbose': False,
    }
    if proxy == 'y':
        host['ssh_config_file'] = '~/.ssh/proxy.config',

    return host


#-------------------------------------------#
# Create table header with hostname/IP      |
#-------------------------------------------#
def table_header(name):
    host_string = ('|   ' + name + '        |')
    header_string = '+'
    for letter in range(len(host_string)-2):
        header_string = header_string + '-'
    header_string = header_string + '+'
    print(header_string)
    print(host_string)