# read commandline inputs/user
import argparse
argParser = argparse.ArgumentParser()
argParser.add_argument("-ID", "--testID", help="input the Test ID")
argParser.add_argument("-PanS", "--PanelSource", help="input the Test ID")

args = argParser.parse_args()
testID = args.testID
PanelSource = args.PanelSource 


if testID[:1] != "R":
    print("invalid R code")


# get info from test directory

import pandas as pd

test_code="R67"


# get an excel into a pandas dataframe, getting specific columns
xls = 'Rare-and-inherited-disease-national-genomic-test-directory-version-5.1.xlsx'
test_directory_df = pd.read_excel(xls, 'R&ID indications', usecols="A:E", header=1)

# get rows with a matching test code
panel = test_directory_df.loc[test_directory_df['Clinical indication ID'] == test_code]

# print columns
print(panel['Target/Genes'].to_string(index=False))

test_code="R67"

# get an excel into a pandas dataframe, getting specific columns
xls = 'Rare-and-inherited-disease-national-genomic-test-directory-version-5.1.xlsx'
test_directory_df = pd.read_excel(xls, 'R&ID indications', usecols="A:E", header=1)

# get rows with a matching test code
panel = test_directory_df.loc[test_directory_df['Clinical indication ID'] == test_code]

# print column of interest
print(panel['Target/Genes'].to_string(index=False))



# use test directory info for building an API





# return desired output
