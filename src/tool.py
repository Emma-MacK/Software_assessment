# read commandline inputs/user
import argparse
import pandas as pd
import requests
from parseJsonPanelAppScript import parseJsonPanelAppFunction

argParser = argparse.ArgumentParser()
argParser.add_argument("-ID", "--testID", help="input the Test ID")
argParser.add_argument("-PanS", "--PanelSource", help="input the Test ID", choices=['NGTD','PanelApp'])
args = argParser.parse_args()
testID = args.testID
PanelSource = args.PanelSource 
# this code creates an argument parser that takes in the testID and panel source

if testID[:1] != "R":
    print("invalid R code")

if PanelSource == "NGTD":
    # get an excel into a pandas dataframe, getting specific columns
    xls = 'Rare-and-inherited-disease-national-genomic-test-directory-version-5.1.xlsx'
    test_directory_df = pd.read_excel(xls, 'R&ID indications', usecols="A:E", header=1)

    # get rows with a matching test code
    panel = test_directory_df.loc[test_directory_df['Clinical indication ID'] == testID]

    # print columns
    print(panel['Target/Genes'].to_string(index=False))

elif PanelSource == "PanelApp":
    # use test directory info for building an API

    # panelapp server
    server = "https://panelapp.genomicsengland.co.uk/api/v1"
    # insert R code 
    ext = "/panels/" + testID

    # adds server and ext with id 
    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})

    #parsesData and returns a dataframe
    genePanelDataframe = parseJsonPanelAppFunction(r,False)
    hgnc_IDs_list = genePanelDataframe.get('hgnc_IDs').to_list()
    # you can access hgnc_IDs through: genePanelDataframe['hgnc_IDs']

else:
    print("Valid options are NGTD or PanelApp")