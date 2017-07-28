# NetSpark-Scripts

## What is the purpose?
This repo will hold the cleaned scripts I've made for simplifying repetitive tasks. I'll be making use of Kirk Byers' Netmiko project to hopefully cut down on the work needed to mass-run commands.

## What is the target audience?
Any network administrator who's sick of manually touching things! These are certainly not meant as a replacement for configuration management, NCM, or other products of the like. This is for stuff where we'll be parsing output, making intelligent programmed changes, etc.

## What are the requirements?
* Netmiko
* TinyDB (For DB support)
* pyperclip (for formatCW.py script)
* getpass (for secure password grabbing)

Everything else should be in stdlib.

## What are the scripts/what do they do?

#### Cisco Command Scripts
The majority of scripts use base_script_model.py as a template. They log into switches fed to them from a csv file, run the commands and sometimes perform logic on the returned information to produce what's needed. The basic script I point everyone to is findMAC.py, which lets you map a mac address to a port. VERY useful when finding which port a phone is plugged into or something along those lines.

#### Other Processing Scripts
There's scripts here for adding information to a database (TinyDB), formatting email updates to a Connectwise ticket handler, and processing the relevant data out of a FortiAnalyzer report. 'fortiport.py' is one you should check out as it works with an .ini file, whcih is where I'll eventually move all of these to go (or JSON...haven't decided).

## Future Automation Projects
+ A script that takes a MAC address, finds its port/VLAN amongst a number of switches, and sets up an ERSPAN to a Wireshark VM.
+ Push out config changes to all or select devices as a one time change (using Ansible)
+ Create config templates that compare device configs to the standard and automate the updates of those devices (automated remediation, the fifth level of Stretch's Hierarchy of Network Needs: http://packetlife.net/blog/2015/dec/14/stretchs-hierarchy-network-needs/)
+ One click provisioning of new devices into all of our various other tools. No more forgetting to update the device in the monitoring server (Nagios plugins for this to come)
+ Updates device information in other monitoring tools if the device changes (IPAM tools)
+ ~~Collects backups of all network devices~~ Completed with automated backup scheduling tool tftpBackups.py 12/8/16
+ Map vlans -> subnets, subnets -> vrfs, MAC addresses -> switchports, IP addresses, VLANs
+ Gather historical CDP info (requires TinyDB)
+ Allows a user to put in two hosts and it will trace the path that the packets take and provide: VRF information, firewall information, and physical ports taken
+ Periodic change of your local passwords; have a script use the API of your enterprise password management suite to login with the current local password, request a new one, change it, and save the config (Postponed until I can dig into API's for Keypass, LastPass, and Thycotic)
+ Automatic interface descriptions. Get the MAC address from the port, query the layer 3 termination for the IP address of the endpoint, and label the interface with the hostname of the device from rDNS or from a powershell query or something.

##### LONG TERM POTENTIAL:
Switch boots, pulls a DHCP address, is told by a DHCP attribute to pull a generic config file that contains an event script that fires after a couple of minutes. That script uses LLDP to figure out what his parent switch is, and what port he's connected to. Armed with the knowledge of what kind of device you are, who you're connected to and what port you'e talking to, you can construct a unique association with a config file without any advanced knowledge about the switch you're deploying. The switch would then pull its "real" config from the TFTP server, and register itself with an inventory management system.
