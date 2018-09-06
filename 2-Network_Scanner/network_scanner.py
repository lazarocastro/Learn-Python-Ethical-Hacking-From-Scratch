#!/usr/bin/env python

import scapy.all as scapy
import optparse

class color:
    END     = '\033[0m' 
    WHITE   = '\033[0;30m' 
    RED     = '\033[0;31m' 
    GREEN   = '\033[0;32m' 
    YELLOW  = '\033[0;33m' 
    BLUE    = '\033[0;34m' 
    PURPLE  = '\033[0;35m' 
    OCEAN   = '\033[0;36m' 
    GRAY    = '\033[0;37m' 
    WHITE_BOLD   = '\033[1;30m' 
    RED_BOLD     = '\033[1;31m' 
    GREEN_BOLD   = '\033[1;32m' 
    YELLOW_BOLD  = '\033[1;33m' 
    BLUE_BOLD    = '\033[1;34m' 
    PURPLE_BOLD  = '\033[1;35m' 
    OCEAN_BOLD   = '\033[1;36m' 
    GRAY_BOLD    = '\033[1;37m' 

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Target IP / IP range. Ex.: 10.0.0.1/24")
    (options, arguments) = parser.parse_args()
    if not options.target:
        parser.error(color.RED_BOLD + "[-] Please specify a target that you want to scan. Ex.: 10.0.0.1/24 or --help for more info." + color.END)
    return options

def scan(ip):
    print(color.GREEN_BOLD + "[+] Scanning Network " + color.END + ip)
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    
    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

def print_result(results_list):
    count = 0
    if results_list:
        print("IP\t\t\tMAC Address\n-----------------------------------------")
        for client in results_list:
            print(client["ip"] + "\t\t" + client["mac"])
            count += 1
        print(color.GREEN_BOLD + "[+] Targets found: " + color.END + str(count))
    else:
        print(color.RED_BOLD + "[-] Network can't be scanning." + color.END)

options = get_arguments()
scan_result = scan(options.target)
print_result(scan_result)
