import argparse
# read commandline inputs/user
argParser = argparse.ArgumentParser()
argParser.add_argument("-ID", "--testID", help="input the Test ID")
argParser.add_argument("-PanS", "--PanelSource", help="input the Test ID")

args = argParser.parse_args()
testID = args.testID
PanelSource = args.PanelSource


if testID[:1] != "R":
    print("invalid R code")


# get info from test directory 





# use test directory info for building an API





# return desired output
