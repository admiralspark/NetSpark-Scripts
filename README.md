<h1 align="center">Netspark-Scripts</h1>

<p align="center">Networking scripts to assist Network Engineers around the world!</p>

## Table of Contents

    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Usage](#usage)
    - [Contributing](#contributing)
    - [Acknowldegements](#acknowledgements)

## Prerequisites

For everything:

```pip install netmiko tinydb pyperclip getpass```

For the network scripts:

```pip install netmiko```

For database support (WIP):

```pip install tinydb```

For the email formatter (connectwise):

```pip install pyperclip```

For secure credential access (req'd soon):

```pip install getpass```

## Installation

Clone the repo, and run the scripts using Python 3. This is NOT a library or module, it is meant to be templates and examples that you can use, copy, and make better.

## Usage

Create your 'customer' file and 'credentials' file based on exampleCSV.md. Then, run the scripts, filling in info as you go!

## Contributing

All patches welcome! Please read [CONTRIBUTING.md](https://github.com/admiralspark/netspark-scripts/CONTRIBUTING.md) for furthers details.

## License

GNU GPL Version 3 - see the [LICENSE](https://github.com/admiralspark/netspark-scripts/LICENSE) file for details

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
