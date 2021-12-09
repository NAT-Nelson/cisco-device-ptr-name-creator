from netmiko import ConnectHandler
import csv
import datetime

# Read in device_list and iterate through it to build a list of IP's
with open('device_list', 'r',) as device_list_file:
    device_list = []
    for ip in device_list_file:
        ip_strip = ip.strip()
        device_list.append(ip_strip)

for device_ip in device_list:
    dev = {
        'device_type': 'cisco_ios',
        'ip': device_ip,
        'username': 'admin',
        'password': 'access123',
        'secret': 'access123',
    }
    print("########## Connecting to Device {0} ##########".format(dev['ip']))
    try:
        net_connect = ConnectHandler(**dev)
    except:
        print("oops, I did it again")
        continue

    net_connect.enable()

    print("***** Sending Show Commands to Device *****")
    device_name = net_connect.find_prompt().strip("#")
    raw_output = net_connect.send_command("show ip int brief")
    list_output = raw_output.splitlines()
    my_dict = {}
    for i in list_output:
        itemized = i.split()
        if "Interface" not in itemized:
            if itemized:
                my_dict.update({itemized[0]: itemized[1]})
        if "unassigned" in my_dict.values():
            my_dict.popitem()
    reverse_dns_name = []

    for key in my_dict:
        int_name = key
        ip = my_dict[key]
        reverse_dns_name.append(f"{device_name}-{int_name}-{ip}")

    reverse_dns_name_no_slashes = []
    for i in reverse_dns_name:
        reverse_dns_name_no_slashes.append(i.replace('/', '-'))  # R1-GigabitEthernet0-0-192.168.100.129
    print(reverse_dns_name_no_slashes)

    with open('reverse_dns_names.csv', 'a', newline='') as csv_1:
        csv_out = csv.writer(csv_1)
        # If the date and time is needed this can be uncommented
        # now = str(datetime.datetime.now())
        # csv_out.writerow([now])
        for item in reverse_dns_name_no_slashes:
            ip_list = item.split('-')
            ip = ip_list[-1]
            csv_out.writerow([item + ',' + ip])


# for index in range(0, len(reverse_dns_name_no_slashes)):
# csv_out.writerows([reverse_dns_name_no_slashes[index]] for index in range(0, len(reverse_dns_name_no_slashes)))



