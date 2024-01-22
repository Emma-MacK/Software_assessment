# read commandline inputs/user
import argparse
import json
import logging
import logging.config
import time
from functions import get_target_panelapp, check_testID, check_ngtd

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
argParser.add_argument("-ID", "--testID", help="input the Test ID", required=True)

# parsing the commandline argument and saving it to a variable.
args = argParser.parse_args()
testID = args.testID
logging.info("Request received for %s panel", testID)

# specifying location of NGTD file and saving all files to variable files.
# NGTD file available in repo is from version 5.1. of the genomic test
NGTD_DIRECTORY = 'test_directory_file'
# TODO: Consider changing file location to a mounted volume when implementing docker.

# specifyng generic NGTD download link which can be modified by adding X.X.xlsx where X stands for a number
NGTD_LINK = "https://www.england.nhs.uk/wp-content/uploads/2018/08/Rare-and-inherited-disease-national-genomic-test-directory-version-"

ngtd_status, version = check_ngtd(NGTD_DIRECTORY, NGTD_LINK)
print(ngtd_status) # TODO: This doesn't necessarily need to print. it could just go to logging.

# using check_testID function to confirm user input
confirmed_testid = check_testID(testID)
logging.info(confirmed_testid)

# pulling panel information from PanelApp Api
genes_panelapp = get_target_panelapp(testID)

# Loading json into a dictionary and logging panel name
genes_panelapp_dict = json.loads(genes_panelapp)
panel_name = genes_panelapp_dict.get("name")
print(f"Panel information pulled for {testID}:{panel_name}")
logging.info("Successfully pulled data for %s:%s", testID, panel_name)