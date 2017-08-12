'''
This script is dead simple--it formats the commands to add a single
IP to the blacklist
'''

IPADDR = input("What is the IP you wish to block? ")
IPBL = "Ext.Blacklist." + IPADDR
print("\n------------------------------------------------------------\n")
print("show firewall address " + IPBL)
print("\n------------------------------------------------------------")
print("------------------------------------------------------------\n")
print("config firewall address")
print("  edit \"" + IPBL + "\"")
print("    set comment \"" + IPBL + " via CLI\"")
print("    set subnet " + IPADDR + " 255.255.255.255")
print("end")
print("\n------------------------------------------------------------")
print("------------------------------------------------------------\n")
print("config firewall addrgrp")
print("  edit \"Ext.Blacklist\"")
print("    append member " + IPBL)
print("end")
print("\n------------------------------------------------------------")
print("------------------------------------------------------------\n")
print("show firewall addrgrp Ext.Blacklist")
print("\n------------------------------------------------------------")
