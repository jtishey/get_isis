#!/usr/bin/env python
'''
get_isis.py
SSH to router and gets interfaces
with ISIS adjacencies, then reports
the current traffic and metric for each

github.com/jtishey/get_isis
'''

from modules import get_host

if __name__ == "__main__":
    host = get_host()
    if host['device_type'] == 'juniper':
        import junos
        junos.execute(host)
    elif host['device_type'] == 'cisco_ios':
        import cisco_ios
        cisco_ios.execute(host)
    elif host['device_type'] == 'cisco_xr':
        import cisco_xr
        cisco_xr.execute(host)
