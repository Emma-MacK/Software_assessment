# read commandline inputs/user
import argparse
import logging
import logging.config
import logging.handlers as handlers
import time
import pandas as pd
import requests
from functions import get_target_ngtd, get_target_panelapp, check_testID, check_ngtd

# setting the logging.Formatter to use GMT time as default.
# Guarantees that the log file always reflects UK local time
logging.Formatter.converter = time.gmtime

# loading logging configuration from the file
logging.config.fileConfig('config/logging.conf')

# create or get logger
logger = logging.getLogger()

argParser = argparse.ArgumentParser()
argParser.add_argument("-ID", "--testID", help="input the Test ID", required=True)

# parsing the commandline argument and saving it to a variable.
args = argParser.parse_args()
testID = args.testID

# specifying location of NGTD file and saving all files to variable files.
# NGTD file available in repo is from version 5.1. of the genomic test
NGTD_DIRECTORY = 'test_directory_file'
# TODO: Consider changing file location to a mounted volume when implementing docker.

# specifyng generic NGTD download link which can be modified by adding X.X.xlsx where X stands for a number
NGTD_LINK = "https://www.england.nhs.uk/wp-content/uploads/2018/08/Rare-and-inherited-disease-national-genomic-test-directory-version-"

ngtd_status, version = check_ngtd(NGTD_DIRECTORY, NGTD_LINK)
print(ngtd_status) # TODO: This doesn't necessarily need to print. it could just go to logging.

# running check_testID function to confirm that the test ID has been provided
# in a valid format and can be found in the current version of the national
# genomic test directory
print(check_testID(testID, NGTD_DIRECTORY, version))

# pulling list of genes from PanelApp API
genes_panelapp = get_target_panelapp(testID)
print(genes_panelapp)