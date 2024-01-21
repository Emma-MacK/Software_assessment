# read commandline inputs/user
import argparse
import logging
import logging.config
import time
from functions import get_target_panelapp, check_testID

# setting the logging.Formatter to use GMT time as default.
# Guarantees that the log file always reflects UK local time
logging.Formatter.converter = time.gmtime

# loading logging configuration from the file
logging.config.fileConfig('config/logging.conf')

# create/get logger
logger = logging.getLogger()

# creating an ArgumentParser to handle command-line arguments
# adding -ID/--testID as an mandatory input
argParser = argparse.ArgumentParser()
argParser.add_argument("-ID", "--testID", help="input the Test ID")

# parsing the commandline argument input and saving it to variable testID
args = argParser.parse_args()
testID = args.testID

# using check_testID function to confirm user input
print(check_testID(testID))

# pulling panel information from PanelApp Api
genes_panelapp = get_target_panelapp(testID)
print(genes_panelapp)