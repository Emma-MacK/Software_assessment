# read commandline inputs/user
import argparse
import logging
import logging.config
import time
from functions import check_testID, get_target_panelapp

# setting the logging.Formatter to use GMT time as default.
# Guarantees that the log file always reflects UK local time
logging.Formatter.converter = time.gmtime

# loading logging configuration from the file
# Relative path
logging.config.fileConfig('../../../config/logging.conf')
# create or get logger
logger = logging.getLogger()

argParser = argparse.ArgumentParser()
argParser.add_argument("-ID", "--testID", help="input the Test ID")

args = argParser.parse_args()
testID = args.testID

print(check_testID(testID))

genes_panelapp = get_target_panelapp(testID)
print(genes_panelapp)
