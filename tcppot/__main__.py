"""
TCP pot.

Simple TCP honeypot logger for Pi

Usage:
    tcppot --config File

Options:
    --config File path to config option .ini file
    -h --help display this screen
"""

import configparser
import logging
import sys
from subprocess import call
from tcppot import HoneyPot

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if len(sys.argv) < 2:
    print(__doc__)
    sys.exit(1)

if sys.argv[1] in ['-h', '--help']:
    print("""To install the tcppot.
use Python -m tcppot.
after completing the installation one can use the package by
python -m tcppot tcppot.ini
one can simply download this package for python
using pip install tcppot""")
    sys.exit(1)

# Load config
config_filepath = "tcppot.ini"
# and "var/lib/log/tcppot.ini"
config = configparser.ConfigParser()
config.read(config_filepath)

ports = config.get('default', 'ports', raw=True, fallback="7771,7772,9999")
host = config.get('default', 'host', raw=True, fallback="0.0.0.0")
log_filepath = config.get('default', 'logfile', raw=True, fallback="tcppot.log")


# print("test")
logger.info("ports: %s" % ports)
logger.info("Logfile: %s" % log_filepath)

# need to make tcppot

ports_list = []
try:
    ports_list = ports.split(',')
except Exception as e:
    logger.info("Error Parsing the port %s.\n Exiting!.....", ports)
    sys.exit(1)

honeypot = HoneyPot(host, ports_list, log_filepath)
honeypot.run()
