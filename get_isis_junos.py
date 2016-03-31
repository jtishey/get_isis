def juniper(host):
    
    from netmiko import ConnectHandler
    from prettytable import PrettyTable
    from modules import ReadableRate
    import re
    
    interface, neighbor = "",""
    rx,tx = "",""
    table = PrettyTable(['Interface','In','Out','Neighbor','Metric','Total_Traffic'])
    
    net_connect = ConnectHandler(**host)
    isis_int = net_connect.send_command("show isis adjacency | match Up")
    isis_int = isis_int.splitlines()
    while '' in isis_int:
        isis_int.pop(isis_int.index(''))
    while '{master}' in isis_int:
        isis_int.pop(isis_int.index('{master}'))
    for line in isis_int:
        total_traffic = 0
        # Extract neighbor and interface
        for item in line.split():
            if re.search("..\-[0-9]+/[0-9]+/[0-9+]", item) != None or re.search("^ae", item) != None:
                interface = item
            elif len(item) > 4:
                if re.search("..\:..\:..\:..",item) == None:
                    neighbor = item
        # Get interface traffic
        show_int = net_connect.send_command("show interface " + interface.split('.')[0] + ' | match "put rate"')
        show_int = show_int.splitlines()
        while '' in show_int:
            show_int.pop(show_int.index(''))
        for l in show_int:
            counter = 0
            for thing in l.split():
                if thing != 'bps':
                    counter+=1
                else:
                    if "Input" in l:
                        rx = ReadableRate(int(l.split()[counter-1]))
                        total_traffic = total_traffic + int(l.split()[counter-1])
                    elif "Output" in l:
                        tx = ReadableRate(int(l.split()[counter-1]))
                        total_traffic = total_traffic + int(l.split()[counter-1])
        # Get isis metric
        show_isis = net_connect.send_command("show isis interface | match " + interface)
        show_isis = show_isis.splitlines()
        while '' in show_isis:
            show_isis.pop(show_isis.index(''))
        for metric_line in show_isis:
            for word in metric_line .split():
                if re.search("[0-9]+/[0-9]+", word) != None:
                    metric = word
        table.add_row([interface,rx.rate,tx.rate,neighbor,metric,(total_traffic*-1)])
    
    net_connect.disconnect()
    print(table.get_string(sortby='Total_Traffic'))