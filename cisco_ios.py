def execute(host):
    
    from netmiko import ConnectHandler
    from prettytable import PrettyTable
    from modules import ReadableRate
    from modules import table_header
    import re
    
    interface, neighbor = "",""
    rx,tx = "",""
    table = PrettyTable(['Interface','In','Out','Neighbor','Metric','Total_Traffic'])
    
    net_connect = ConnectHandler(**host)
    isis_int = net_connect.send_command("show isis neighbor | i L2")
    isis_int = isis_int.splitlines()
    while '' in isis_int:
        isis_int.pop(isis_int.index(''))
    for line in isis_int:
        total_traffic = 0
        # Extract neighbor and interface
        for item in line.split():
            if re.search("^[Fa|Gi|Te|Hu|Po|Vl]", item) != None:
                interface = item
            neighbor = line.split()[0]
            neighbor = neighbor.replace('-re0','')  # Don't care about Junipers with apply-
            neighbor = neighbor.replace('-re1','')  # groups to append active RE to hostname
        # Get interface traffic
        show_int = net_connect.send_command("show interface " + interface.split('.')[0] + " | include put rate")
        show_int = show_int.splitlines()
        while '' in show_int:
            show_int.pop(show_int.index(''))
        for lines in show_int:
            counter = 0
            for thing in lines.split():
                if re.search("bits",thing) == None:
                    counter+=1
                else:
                    counter -=1
                    if "nput" in lines:
                        rx = ReadableRate(int(lines.split()[counter]))
                        total_traffic = total_traffic + int(lines.split()[counter])
                        counter +=1
                    elif "utput" in lines:
                        tx = ReadableRate(int(lines.split()[counter]))
                        total_traffic = total_traffic + int(lines.split()[counter])
                        counter +=1
        # Get isis metric
        show_isis = net_connect.send_command("show clns interface " + interface + " | include Metric")
        show_isis = show_isis.splitlines()
        while '' in show_isis:
            show_isis.pop(show_isis.index(''))
        for lines in show_isis:
            counter = 0
            for word in lines.split():
                if re.search("Metric", word) != None:
                    metric = lines.split()[counter+1]
                    metric = metric.split(',')[0]
                counter +=1
        table.add_row([interface,rx.rate,tx.rate,neighbor,metric,(total_traffic*-1)])
    
    net_connect.disconnect()
    table_header(host['ip'])
    print(table.get_string(sortby='Total_Traffic'))