<h1 align="center">Netspark-Scripts</h1>

<p align="center">Multithreaded parallel network command execution, simplified, for network engineers of the world!</p>

![Python](https://img.shields.io/badge/Python-3.4%2C%203.5%2C%203.6-green.svg)

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## Prerequisites

For everything:

```pip install netmiko docopt getpass```

## Installation

Clone the repo, and run the scripts using Python 3. This is NOT a library or module, it is meant to be templates and examples that you can use, copy, and make better.

## Usage

Create your 'customer' file and 'credentials' file based on exampleCSV.md.

### python netspark.py -h
This script is the master controller script. It will make the necessary
commands to run whatever is needed against whatever is needed.

    Usage:
        netspark.py -h | --help
        netspark.py (--info COMMAND | --config CONFIGFILE) (--csv FILENAME | --db QUERYNAME | --ip IPADDR) [-c CREDFILE] [--debug]

    Options:
        -h, --help          Shows this menu.
        -d, --debug         Print debug information. This is the most verbose
                            option.
        --info COMMAND   This will run regular show commands
        --config CONFIGFILE This will run configuration commands
        --csv FILENAME      Input file if using CSV [default: test.csv]
        --db QUERYNAME      SQL field: 'groupname' [default: test]
        --ip IPADDR         Single IP address of test switch
        -c CREDFILE         Crednetials file [default: credentials.csv]

### Examples:
To run write mem on every host in your csv file switches.csv (assuming you only have one credentials.csv):

`python netspark.py --info "wr mem" --csv switches.csv`

To make a config change with many lines, such as changing a local account, you'd make a text file with the lines to change it which will then be run against the hosts. For example, lets make a changeuser.txt:

```
exit
conf t revert time 5
username secretbackdoor privilege 15 password Thiscantbereal!
```

Then you'd run it like so: `python netspark.py --config changeuser.txt --csv switches.csv`

This command supports all of the netmiko classes of devices, but I designed it to be used with Cisco gear since that's what most of us run. You just need to specify a different device object in your switches.csv file to work with new stuff.

Final example, lets say you have a rogue sysadmin at one branch who refuses to use newer credentials/radius/whatever. So you have a different nonstandard set of creds and routers.

`python netspark.py --info "configure confirm" --csv crappyrouters.csv -c crappycreds.csv`

### Caveats

This is multithreaded and I haven't added error handling. I force all of my changes to use config revision (the 'conf t revert time 5' above) as a workaround until I have good error handling in place. It's laziness and a lack of time, it would be decently easy to implement.

The multiprocess code I wrote is messy because of context issues. I plan on making that part into a library later on, but something something time and laziness.

The default number of simultaneous executions is 8, I have run this successfully at 50x simultaneous on a network of 400+ devices but keep in mind that they will return output at a rate of 50x, and it spits it out to STDOUT, so you might want to just leave it.

I will add support for --db and --ip later on, probably --db first because I want this to dive into the rest of my open-source stack I'm slowly writing about on https://teamignition.us so that this all ties in beautifully.

## The Example_Scripts folder
This is old code and alternative projects. It is useful reference material so I'm leaving it up, but it will not be updated.

## Contributing

All patches welcome! Please read [CONTRIBUTING.md](https://github.com/admiralspark/netspark-scripts/CONTRIBUTING.md) for furthers details...whenever I make it. For now, submit PR's and we'll chat about them.

## License

GNU GPL Version 3 - see the [LICENSE](https://github.com/admiralspark/NetSpark-Scripts/blob/master/LICENSE) file for details
