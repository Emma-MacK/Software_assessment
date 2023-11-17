# read commandline inputs/user
import argparse
import pandas as pd
import requests
from functions import get_target_ngtd, get_target_panelapp

argParser = argparse.ArgumentParser()
argParser.add_argument("-ID", "--testID", help="input the Test ID")
argParser.add_argument("-PanS", "--PanelSource", help="input the Test ID", choices=['NGTD','PanelApp'])

args = argParser.parse_args()
testID = args.testID
PanelSource = args.PanelSource


if testID[:1] != "R":
    print("invalid R code")

if PanelSource == "NGTD":
    genes_ngtd = get_target_ngtd(testID)
    print(genes_ngtd)

elif PanelSource == "PanelApp":
    genes_panelapp = get_target_panelapp(testID)
    print(genes_panelapp)
else:
    print("Valid options are NGTD or PanelApp")
