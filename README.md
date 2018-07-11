<h1 align="center">Netspark-Scripts</h1>

<p align="center">Networking scripts to assist Network Engineers around the world!</p>

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

To make a 

## Contributing

All patches welcome! Please read [CONTRIBUTING.md](https://github.com/admiralspark/netspark-scripts/CONTRIBUTING.md) for furthers details.

## License

GNU GPL Version 3 - see the [LICENSE](https://github.com/admiralspark/NetSpark-Scripts/blob/master/LICENSE) file for details
