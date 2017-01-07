def execute(host):

    from netmiko import ConnectHandler
    from prettytable import PrettyTable
    from modules import ReadableRate
    from modules import table_header
    import re

    interface, neighbor = "", ""
    rx, tx = "", ""
    table = PrettyTable(['Interface', 'In', 'Out', 'Neighbor', 'Metric', 'Total_Traffic'])
    net_connect = ConnectHandler(**host)
    isis_int = net_connect.send_command("show isis neighbor | i L2")
    isis_int = isis_int.splitlines()
    while '' in isis_int:
        isis_int.pop(isis_int.index(''))
    for line in isis_int:
        total_traffic = 0
        # Extract neighbor and interface
        for item in line.split():
            if re.search("^[Fa|Gi|Te|Hu|Po|Vl]", item) is not None:
                interface = item
            neighbor = line.split()[0]
            neighbor = neighbor.replace('-re0', '')  # Don't care about Junipers with apply-
            neighbor = neighbor.replace('-re1', '')  # groups to append active RE to hostname
        # Get interface traffic
        show_int = net_connect.send_command("show interface " + interface.split('.')[0] + " | include put rate")
        for lines in show_int.splitlines():
            for i, word in enumerate(lines.split()):
                if 'bits' in word:
                    traf = int(lines.split()[i - 1])
                    total_traffic = total_traffic + traf
                    if 'nput' in lines:
                        rx = ReadableRate(traf)
                    elif "utput" in lines:
                        tx = ReadableRate(traf)
        # Get isis metric
        show_isis = net_connect.send_command("show clns interface " + interface + " | include Metric")
        show_isis = show_isis.splitlines()
        while '' in show_isis:
            show_isis.pop(show_isis.index(''))
        for i, lines in enumerate(show_isis):
            for word in lines.split():
                if re.search("Metric", word) is not None:
                    metric = lines.split()[i + 1]
                    metric = metric.split(',')[0]
        table.add_row([interface, rx.rate, tx.rate, neighbor, metric, (total_traffic)])
    net_connect.disconnect()
    table_header(host['ip'])
    print(table.get_string(sortby='Total_Traffic', reversesort=True))
