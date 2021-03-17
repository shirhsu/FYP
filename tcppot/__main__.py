"""
TCPpot.

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

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from tcppot import HoneyPot

if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
    print(__doc__)
    sys.exit(1)

# Load config
config_filepath = sys.argv[1]
config = configparser.ConfigParser()
config.read(config_filepath)

ports = config.get('default', 'ports', raw=True, fallback="7775,7776,7777")
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

honeypot = HoneyPot(host, ports_list, log_filepath, )
honeypot.run()
