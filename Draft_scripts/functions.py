# script to hold functions
import pandas as pd
import requests

# Get information from test directory

def get_target_ngtd(testID):
    # get an excel into a pandas dataframe, getting specific columns
    xls = 'Rare-and-inherited-disease-national-genomic-test-directory-version-5.1.xlsx'
    test_directory_df = pd.read_excel(xls, 'R&ID indications', usecols="A:E", header=1)

    # get rows with a matching test code
    panel = test_directory_df.loc[test_directory_df['Clinical indication ID'] == testID]

    # print columns
    result_ngtd = panel['Target/Genes'].to_string(index=False)
    return result_ngtd

# get information from panel app

def get_target_panelapp(testID):

    # panelapp server
    server = "https://panelapp.genomicsengland.co.uk/api/v1"
    # insert R code
    ext = "/panels/" + testID

    # adds server and ext with id
    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})

    #returns data
    decoded = r.json()
    result_panelapp = repr(decoded)
    return result_panelapp

# test user inputs