# read commandline inputs/user
import pandas as pd
import requests
from userinterface.ToolModule import parseJsonPanelAppScript
import os


def tool(testID, PanelSource):
    """
    This is now a module so it can interact with django frontend
    """

    hgnc_IDs_list = None

    if testID[:1] != "R":
        print("invalid R code")

    if PanelSource == "NGTD":
        print(os.getcwd())
        # get an excel into a pandas dataframe, getting specific columns
        path = 'userinterface/ToolModule/'
        xls = 'Rare-and-inherited-disease-national-genomic-test-directory-version-5.1.xlsx'
        test_directory_df = pd.read_excel(path + xls, 'R&ID indications', usecols="A:E", header=1)

        # get rows with a matching test code
        panel = test_directory_df.loc[test_directory_df['Clinical indication ID'] == testID]

        # print columns
        print(panel['Target/Genes'].to_string(index=False))
        value = str("Targeted genes are: "+panel['Target/Genes'].to_string(index=False))
        return value, True
    elif PanelSource == "PanelApp":

        # panelapp server
        server = "https://panelapp.genomicsengland.co.uk/api/v1"

        # insert R code
        ext = "/panels/" + testID

        # adds server and ext with id
        r = requests.get(server+ext, headers={"Content-Type": "application/json"})

        # parsesData and returns a dataframe
        genePanelDataframe = parseJsonPanelAppScript.parse_json_panelapp(r, False)

        if isinstance(genePanelDataframe, pd.DataFrame):
            # accessing hgnc_IDs and placing them in a dataframe
            hgnc_IDs_list = genePanelDataframe.get('hgnc_IDs').to_list()
            print(hgnc_IDs_list)
            successfulRequest = True
            return hgnc_IDs_list, successfulRequest
        else:
            print("Nothing to return")
            successfulRequest = False
            return hgnc_IDs_list, successfulRequest
    else:
        print("Valid options are NGTD or PanelApp")
        successfulRequest = False
        return hgnc_IDs_list, successfulRequest
