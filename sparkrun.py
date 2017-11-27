'''
This script is the master controller script. It will make the necessary
commands to run whatever is needed against whatever is needed. 

    Usage:
        sparkrun.py -h | --help
        sparkrun.py (--info COMMAND | --config CONFIGFILE) (--csv FILENAME | --db QUERYNAME | --ip IPADDR) [-c CREDFILE] [--debug]
    
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
'''

import logging
from docopt import docopt
import spark_threaded as st


arguments = docopt(__doc__)

# Set logging level https://www.digitalocean.com/community/tutorials/how-to-use-logging-in-python-3
# This is for debugging.
if arguments['--debug'] == True:
    logging.basicConfig(level=logging.DEBUG)
    print("Arguments: \n" + str(arguments))
else:
    logging.basicConfig(level=logging.INFO)

# Global variable MODE stores whether we're running config or not. This is here instead of defined
# in the functions below because I'm going to use it for testing. 
MODE = st.check_config_mode(arguments['--config'])
logging.debug("Value for MODE evaluated to: " + str(MODE))

if MODE is False:
    st.info_command(arguments['--info'], arguments['--csv'], arguments['--db'], arguments['--ip'], arguments['-c'])

elif MODE is True:
    st.config_command(arguments['--config'], arguments['--csv'], arguments['--db'], arguments['--ip'], arguments['-c'])

else:
    logging.info("You somehow broke the required info/config arguments!")