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
    no_prompt = net_connect.send_command("terminal exec prompt no-timestamp")
    isis_int = net_connect.send_command("show isis neighbor | include Up")
    isis_int = isis_int.splitlines()
    while '' in isis_int:
        isis_int.pop(isis_int.index(''))
    for line in isis_int:
        total_traffic = 0
        # Extract neighbor and interface
        for item in line.split():
            if re.search("[0-9]+/[0-9]+/[0-9]+/[0-9+]", item) != None:
                interface = item
            elif re.search("^BE", item) != None:
                interface = 'Bundle-Ether' + item[2:len(item)]
        neighbor = line.split()[0]
        neighbor = neighbor.replace('-re0','')  # Don't care about Junipers with apply-
        neighbor = neighbor.replace('-re1','')  # groups to append active RE to hostname
        # Get interface traffic
        show_int = net_connect.send_command("show interface " + interface.split('.')[0] + ' | include "put rate"')
        show_int = show_int.splitlines()
        for lines in show_int:
            counter = 0
            for word in lines.split():
                if re.search("bits",word) == None:
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
        show_isis = net_connect.send_command("show isis interface " + interface + " | include Metric")
        show_isis = show_isis.splitlines()
        for lines in show_isis:
            for word in lines .split():
                if re.search("[0-9]+/[0-9]+", word) != None:
                    metric = word
        table.add_row([interface,rx.rate,tx.rate,neighbor,metric,(total_traffic*-1)])
    
    net_connect.disconnect()
    table_header(host['ip'])
    print(table.get_string(sortby='Total_Traffic'))