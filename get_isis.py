#!/usr/bin/env python
'''
get_isis.py
SSH to router and gets interfaces
with ISIS adjacencies, then reports
the current traffic and metric for each

github.com/jtishey/get_isis
'''

from modules import get_host

host = get_host()

if host['device_type'] == 'juniper':
    import get_isis_junos
    table = get_isis_junos.juniper(host)
elif host['device_type'] == 'cisco_ios':
    import get_isis_ios
    table = get_isis_ios.cisco_ios(host)
elif host['device_type'] == 'cisco_xr':
    import get_isis_xr
    table = get_isis_xr.cisco_xr(host)