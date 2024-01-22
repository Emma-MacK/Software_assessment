# read commandline inputs/user
import argparse
import logging
import logging.config
import logging.handlers as handlers
import time
import pandas as pd
import requests
from functions import get_target_ngtd, get_target_panelapp, check_testID, get_hgncIDs, call_transcript_make_bed

# setting the logging.Formatter to use GMT time as default.
# Guarantees that the log file always reflects UK local time
logging.Formatter.converter = time.gmtime

# loading logging configuration from the file
logging.config.fileConfig('config/logging.conf')

# create or get logger
logger = logging.getLogger()

argParser = argparse.ArgumentParser()
argParser.add_argument("-ID", "--testID", help="input the Test ID")

args = argParser.parse_args()
testID = args.testID


# TODO: change to commandline arguments
flank = 25
genome_build = "GRCh37"
transcript_set = "refseq"
limited_transcripts = "mane_select"

print(check_testID(testID))

genes_panelapp = get_target_panelapp(testID)
# print(genes_panelapp)

hgnc_list = get_hgncIDs(genes_panelapp)

call_transcript_make_bed(hgnc_list, flank, genome_build,
                             transcript_set, limited_transcripts)
