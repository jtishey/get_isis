# get_isis.py

SSH to Juniper, Cisco IOS, and Cisco IOS-XR routers
and get a list of interfaces with active ISIS adjacencies.
Display these interfaces in a table with the currently
reported interface traffic and IPv4 ISIS metric.

REQUIRES : netmiko, paramiko, prettytable

The default behavior is currently to run with no arguments
and prompt for the following:
  Hostname/IP, Device OS, Username, Password 

Also, get_isis can be used to connect via local SOCKS proxy:

1. Uncomment line 45 in modules.py
2. Create a file in your ~/.ssh/proxy.config as follows:
      echo 'ProxyCommand proxy_cheater %h' > ~/.ssh/proxy.config
3. Create a bash script to fix the IP/port for netcat:
      vim proxy_cheater
      #!/bin/bash
      ADDR="$1"
      HOST=${ADDR%:*}  # get the part before the colon
      PORT=${ADDR##*:}  # get the part after the colon
      /bin/nc -x 127.0.0.1:1080 $HOST $PORT
   (Make it executable and put it in your PATH)
4. Start a local SOCKS proxy connection on 127.0.0.1:1080


EXAMPLE:
$ python get_isis.py 
Hostname/IP:10.0.10.4
Device OS:junos
Username:admin
Password: 
+-----------------------+
|   10.0.10.4           |
+--------------+--------+--------+----------+--------+---------------+
|  Interface   |   In   |  Out   | Neighbor | Metric | Total_Traffic |
+--------------+--------+--------+----------+--------+---------------+
| ge-0/0/4.145 | 11.8 K | 15.6 K |  vSRX5   | 10/10  |     -27408    |
| ge-0/0/4.134 | 12.9 K | 9.9 K  |  vSRX3   | 10/10  |     -22752    |
| ge-0/0/4.114 | 10.4 K | 9.8 K  |  vSRX1   | 10/10  |     -20240    |
+--------------+--------+--------+----------+--------+---------------+
