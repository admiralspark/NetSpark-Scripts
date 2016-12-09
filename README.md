# NetSpark-Scripts

## What is the purpose?
This repo will hold the cleaned scripts I've made for simplifying repetitive tasks. I'll be making use of Kirk Byers' Netmiko project to hopefully cut down on the work needed to mass-run commands.

## What is the target audience?
Any network administrator who's sick of manually touching things! These are certainly not meant as a replacement for configuration management, NCM, or other products of the like. This is for stuff where we'll be parsing output, making intelligent programmed changes, etc.

## What are the scripts/what do they do?

##### findMAC.py
This script uses the output of "show mac add | inc XXX" where XXX is a manually input mac address. The intent is this: if you have an environment with a dozen switches and you need to find out what port a phone/printer/whatever is plugged into and don't want to check each one by hand, this will pop into each one and spit out what it finds.

Now (12/7/16) it will even intelligently tell you which ports are access, which are trunk, and which one is likely the correct port based on collected information.

## Future Automation Projects
+ A script that takes a MAC address, finds its port/VLAN amongst a number of switches, and sets up an ERSPAN to a Wireshark VM.
+ push out config changes to all or select devices as a one time change (rancid-like)
+ create config templates that compare device configs to the standard and automate the updates of those devices
+ One click provisioning of new devices into all of our various other tools. No more forgetting to update the device in the monitoring server
+ Updates device information in other monitoring tools if the device changes
+ Collects backups of all network devices
+ Connects vlans -> subnets, subnets -> vrfs, MAC addresses -> switchports, IP addresses, VLANs
+ Gather historical CDP info
+ Allows a user to put in two hosts and it will trace the path that the packets take and provide, VRF information, firewall information, and physical ports taken
+ Periodic change of your local passwords; have a script use the API of your enterprise password management suite to login with the current local password, request a new one, change it, and save the config.
+ Automatic interface descriptions. Get the MAC address from the port, query the layer 3 termination for the IP address of the endpoint, and label the interface with the hostname of the device from rDNS or from a powershell query or something.

##### LONG TERM
Switch boots, pulls a DHCP address, is told by a DHCP attribute to pull a generic config file that contains an event script that fires after a couple of minutes. That script uses LLDP to figure out what his parent switch is, and what port he's connected to. Armed with the knowledge of what kind of device you are, who you're connected to and what port you'e talking to, you can construct a unique association with a config file without any advanced knowledge about the switch you're deploying. The switch would then pull its "real" config from the TFTP server, and register itself with an inventory management system.
