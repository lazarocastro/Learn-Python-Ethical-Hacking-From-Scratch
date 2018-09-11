#!/usr/bin/env python

import scapy.all as scapy

packet = scapy.ARP(op=2, pdst="10.150.0.249", hwdst="64:1c:67:68:58:37", psrc="10.150.254")
print(packet)
