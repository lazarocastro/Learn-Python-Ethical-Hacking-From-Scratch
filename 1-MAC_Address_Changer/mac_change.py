#!/usr/bin/env python

import subprocess
import optparse
import re

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
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, new_mac) = parser.parse_args()
    if not options.interface:
        parser.error(color.RED_BOLD + "[-] Please especify an interface, use --help for more info." + color.END)
    elif not options.new_mac:
        parser.error(color.RED_BOLD + "[-] Please especify a new MAC, use --help for more info." + color.END)
    return options

def change_mac(interface, new_mac):
    print(color.GREEN_BOLD + "[+] Changing MAC address for "+ color.END + interface + color.GREEN_BOLD + " to " + color.END + new_mac)
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["sudo", "ifconfig", interface, "up"]) 

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print(color.RED_BOLD + "[-] Could not read MAC address." + color.END)

options = get_arguments()

current_mac = get_current_mac(options.interface)
print(color.GREEN_BOLD + "[+] Current MAC = " + color.END + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print(color.GREEN_BOLD + "[+] MAC address was successfully changed to " + color.END + current_mac)
else:
    print(color.RED_BOLD + "[-] MAC address did not get changed." + color.END)

