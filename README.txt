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

1. Line 65 in modules.py specifies an alternate ssh config file ~/.ssh/proxy.config by default
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


If the following Error is seen connecting to Cisco IOS devices:
	paramiko.ssh_exception.SSHException: Error reading SSH protocol banner

 	Edit transport.py near line 487 (something like /usr/local/lib/python2.7/dist-packages/paramiko/transport.py)
 		# synchronous, wait for a result
        self.completion_event = event = threading.Event()
        # delay starting thread for SSH proxies
        event.wait(3)  # MONKEY_PATCH added wait
        self.start()
        while True:

EXAMPLE:
$ python get_isis.py
Hostname/IP:Router1
Device OS:junos
Username:admin
Password: 
+-----------------------+
|   Router1             |
+-------------+---------+---------+-----------------+----------+---------------+
|  Interface  |    In   |   Out   |     Neighbor    |  Metric  | Total_Traffic |
+-------------+---------+---------+-----------------+----------+---------------+
| et-10/0/0.0 |  8.1 G  |  2.6 G  |     Router5     |   1/10   |  10694783640  |
|  et-9/0/0.0 |  4.3 G  |  3.6 G  |     Router3     |   1/10   |   7883159576  |
|  et-8/0/0.0 |  1.7 G  |  2.7 G  |     Router2     |   1/10   |   4395229432  |
|  xe-5/0/3.0 | 281.8 M |  2.5 G  |     Router7     | 10/1022  |   2733322384  |
|  xe-5/0/2.0 | 262.4 M |  2.5 G  |     Router6     | 10/1022  |   2727649592  |
|  xe-5/0/0.0 | 517.7 M | 828.5 M |     Router3     |   10/1   |   1346266480  |
|  xe-0/2/2.0 | 457.0 M | 884.8 M |     Router8     |   10/1   |   1341755448  |
|  xe-5/0/1.0 |  45.7 M | 384.0 M |     Router2     | 10/10000 |   429747192   |
| et-11/0/0.0 | 130.8 M |  50.4 M |     Router9     |   1/1    |   181227360   |
+-------------+---------+---------+-----------------+----------+---------------+
