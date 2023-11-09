# read commandline inputs/user
import argparse
import pandas as pd
import requests
import json

argParser = argparse.ArgumentParser()
argParser.add_argument("-ID", "--testID", help="input the Test ID")
argParser.add_argument("-PanS", "--PanelSource", help="input the Test ID", choices=['NGTD','PanelApp'])

args = argParser.parse_args()
testID = args.testID
PanelSource = args.PanelSource 


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

    #returns data

     #returns data
    #decoded = json.load(r)
    decoded = r.json()
    print(decoded)

    ##response = requests.post(, data =)
    #print(repr(decoded))

    #jsonParsed = pd.DataFrame.from_dict(decoded,orient='index')
    #print(type(decoded["genes"]))    #y = json.loads(decoded)
    decoded_genes =decoded['genes']
    print(decoded_genes.get("gene_data",{}).get('hgnc_symbol'))
    #print(repr(y))

else:
    print("Valid options are NGTD or PanelApp")