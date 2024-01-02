# import modules
import requests
import os
from datetime import datetime
import pandas as pd

def get_file_age_in_days(file_path):
    # Get the file's modification timestamp
    timestamp = os.path.getmtime(file_path)

    # Convert the timestamp to a datetime object
    modification_time = datetime.fromtimestamp(timestamp)

    # Get the current time
    current_time = datetime.now()

    # Calculate the age of the file in terms of months
    age_in_days = (current_time - modification_time).days

    return age_in_days

# Example usage
# file_path = 'bin'
# age_in_days = get_file_age_in_days(file_path)

# print(f"The file at {file_path} is approximately {age_in_days} days old.")

""""""

# Uses request to download excel directly from NGTD website
def ngtd_download(link):
    response = requests.get(link)
    version = link[-8:-5]
    if response.status_code == 200:
        with open(f'NGTDv{version}.xlsx', 'wb') as output:
            output.write(response.content)
    else:
        print ('File not found error') #rudimentary error flag to be replaced by proper error handeling.

# specifying excel download link of current download link
download_link = ("https://www.england.nhs.uk/wp-content/uploads/2018/08/Rare-and-inherited-disease-national-genomic-test-directory-version-5.1.xlsx")

# calling function and saving to variable xls
xls = ngtd_download(download_link)

# # removes file once the relevant data is pulled.
# os.remove(f'NGTDv{version}.xls')


""""checking the version of the existing file. I am getting this from within the file in case I accidentally saved it wrong previously
this might be overkiill though and it could be better to just split the file name. """
"""PREPARE BOTH AND THEN PRESENT TO THE TEAM AND LET THEM PICKC"""


### I AM RUNNING INTO PROBLEMS GETTING IT TO ACCEPTED THE FILE PATH. THE PARSING ITSELF WORKS.
# specifying the directory path
ngtd_path = 'test_directory_file'
# specifying file path
xls = ngtd_path + '/NGTDv5.1.xlsx'

def get_ngtd_version_from_file(file): #remember that variable names don't matter as long as they are defined within the function.
# what matters is the function that is called with the return function. 
    # Loading Columns A of file into a Dataframe
    test_directory_df = pd.read_excel(file, 'R&ID indications', usecols="A", header=0) # COULD TURN THIS INTO A FUNCTION SO THAT WE CAN CALL IT ANYTIME. 

    # Testing load
    # print(test_directory_df.head())

    #extracting data from first row
    test_directory_header = str(test_directory_df.iloc[0])

    #print(test_directory_header)

    split_header = test_directory_header.split(',')
    section_of_header = split_header[1]

    #print(section_of_header)

    section_of_header_clean = section_of_header.strip( )

    #print(section_of_header_clean)

    version = section_of_header_clean[1:4]

    return(version)

# print(get_ngtd_version_from_file(xls))


"""not specifying file directory"""