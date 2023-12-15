# read commandline inputs/user
import argparse
import pandas as pd
import requests
from functions import get_target_ngtd, get_target_panelapp, check_testID

argParser = argparse.ArgumentParser()
argParser.add_argument("-ID", "--testID", help="input the Test ID")

args = argParser.parse_args()
testID = args.testID

print(check_testID(testID))

genes_panelapp = get_target_panelapp(testID)
print(genes_panelapp)