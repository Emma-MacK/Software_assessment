# read commandline inputs/user
import argparse
import json
import logging
import logging.config
import time

import pandas as pd
import requests
from functions import get_target_ngtd, get_target_panelapp, check_testID, check_ngtd, parse_panel_app_json, call_transcript_make_bed, make_panel_json

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


# TODO: change to commandline arguments
flank = 25
genome_build = "GRCh37"
transcript_set = "refseq"
limited_transcripts = "mane_select"

# specifying location of NGTD file and saving all files to variable files.
# NGTD file available in repo is from version 5.1. of the genomic test
NGTD_DIRECTORY = 'test_directory_file'
# TODO: Consider changing file location to a mounted volume when implementing docker.


# specifyng generic NGTD download link which can be modified by adding X.X.xlsx where X stands for a number
NGTD_LINK = "https://www.england.nhs.uk/wp-content/uploads/2018/08/Rare-and-inherited-disease-national-genomic-test-directory-version-"

ngtd_status, version = check_ngtd(NGTD_DIRECTORY, NGTD_LINK)
print(ngtd_status) # TODO: This doesn't necessarily need to print. it could just go to logging.

# using check_testID function to confirm user input
confirmed_testid = check_testID(testID, NGTD_DIRECTORY, version)
logging.info(confirmed_testid)

# pulling panel information from PanelApp Api
genes_panelapp = get_target_panelapp(testID)
# Loading json into a dictionary and logging panel name
genes_panelapp_dict = json.loads(genes_panelapp)
panel_name = genes_panelapp_dict.get("name")
print(f"Panel information pulled for {testID}: {panel_name}")
logging.info("Successfully pulled data for %s:%s", testID, panel_name)

# retrieve HGNC IDs for bed files from json
hgnc_list, id_omim_dictionary, panelid_version = parse_panel_app_json(genes_panelapp, testID)
logging.info("The panel corresponds to version %s", panelid_version)
logging.debug("The following hgncs have been parsed: %s", hgnc_list)
logging.debug("The following omim numbers have been parsed: %s", id_omim_dictionary)
print(id_omim_dictionary)

# Pulling transcript information and making bedfiles
transcript_data = call_transcript_make_bed(hgnc_list, flank, genome_build,
                             transcript_set, limited_transcripts)


# TODO: When integrating database push replace by push to database question. 
create_json = input("Do you want to create a json file [y/n]: ")
while create_json == "":
    if create_json.lower() == "y":
        for hgnc in hgnc_list:
            make_panel_json(hgnc, id_omim_dictionary, panelid_version, transcript_data)
    elif create_json.lower() == "n":
        print("JSON not created")
        exit
    else:
        create_json = input("Please indicated yes or no [y/n]: ")