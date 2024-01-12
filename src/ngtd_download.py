# import modules
import os
import fnmatch
from math import floor
from datetime import datetime
import requests
import pandas as pd

def get_file_age_in_days(file_path):
    """This function will return the age of a file in days based on the specified file path"""
    # Get the file's modification timestamp
    timestamp = os.path.getmtime(file_path)

    # Convert the timestamp to a datetime object
    modification_time = datetime.fromtimestamp(timestamp)

    # Get the current time
    current_time = datetime.now()

    # Calculate the age of the file in terms of months
    age_in_days = (current_time - modification_time).days
    return age_in_days

def get_ngtd_version(file):
    """This function pulls the version of the the NGTD file from within the file."""
    # Loading Columns A of file into a Dataframe
    test_directory_df = pd.read_excel(file, 'R&ID indications', usecols="A", header=0)
    # TODO: Tidy up with the panda call that Emma has already done.

    #extracting and cleaning data from first row
    test_directory_header = str(test_directory_df.iloc[0])
    split_header = test_directory_header.split(',')
    section_of_header = split_header[1]
    section_of_header_clean = section_of_header.strip( )
    version = section_of_header_clean[1:4]

    return version

def update_ngtd(version, file_directory, link):
    """This function attempts to update the version of the NGTD computationally if the current version is nolonger available.
      If it fails it gives the user the option to proceed with existing copy"""
    # NOTE: Had previously tried to do this with a try block but couldn't think through the logic.
    # TODO: Remove print statements and replace with logging
    # Some elements of this function are bit repetetive and could maybe we streamlined into another function

    # update version number assuming a minor change has been made
    print(version)
    version_new = round(version + 0.1, 1)
    print(version_new)

    update_status = ""

    # Use request to try and obtain a copy of the file with an updated version number.
    response = requests.get(link + f"{version_new}.xlsx", timeout=60)
    # TODO: Add logging to record the version number tried.
    # TODO: Add error handeling for the timeout
    if response.status_code == 200:
        print(response.status_code)
        # TODO: Add logging to record response code and that this means file is still current.
        with open(f'NGTDv{version_new}.xlsx', 'wb') as output:
            output.write(response.content)
        update_status = "passed"

    # Try to see if a copy of the file can be obtained assuming a major update has been made.
    elif response.status_code == 404:
        print(response.status_code)
        version_new = floor(version) + 1.0 # TODO: This can not be tested because no major update is currently available. I will need to test with logging
        # TODO: Add logging to record the version number tried.
        print(version_new)
        response = requests.get(link + f"{version_new}.xlsx", timeout=60)
        if response.status_code == 200:
            # TODO: Add logging to record response code. Do this throughout this function
            with open(f'NGTDv{version_new}.xslx', 'wb') as output:
                output.write(response.content)
            update_status = "passed"
                # TODO: Check where the output file is being written to.
        elif response.status_code == 404:
            version_new = int(version_new)
            print(version_new)
            response = requests.get(link +f"{version_new}.xlsx", timeout=60)
            if response.status_code == 200:
                path_new_file = os.path.join(file_directory, f"NGTDv{version_new}.xlsx")
                print(response.status_code)
                with open(path_new_file, 'wb') as output:
                    output.write(response.content)
                update_status = "passed"
            else:
                update_status = "failed"

    return update_status, version_new # TODO: Test if this actually returns back to the else statement or not.

    # Asks the user whether to proceed with the existing version of the NGTD if it fails to get an updated version.
    # else:

    # return # TODO: Does this successfully exit the function and move on?

def check_ngtd(file_directory, link):
    """This function checks the age of the existing NGTD version, if older than 30 days it will check whether the NGTD version
      is still valid (i.e. available for download)"""

    # For each file in directory checks how old the file is. If older than 30 days check if NGTD version available.
    # N.b. there should only be one file here but this saves having to specify what type of file to look for.
    ngtd_status = ""
    files = os.listdir(file_directory)
    # searching for NGTD file. Note there should only ever be one file in here but this prevents having to specify a
    # specific file and prevents calling any hidden files by accident.
    file_name_pattern = 'NGTD*.xlsx'
    matching_files = fnmatch.filter(files, file_name_pattern)

    for file in matching_files:
        # TODO: Remove all the print statements and replace with logging.
        ngtd_path = os.path.join(file_directory, file)
        # TODO: For loop might be excessive since we only expect one file. Also what happens if there is more than one file?
        if get_file_age_in_days(ngtd_path) < 30:
            # TODO: Add logging of file age
            print('File is less than 30 days old')
            continue
        elif get_file_age_in_days(ngtd_path) >= 30:
            # TODO: Add logging of file age
            print('File is older than 30 days old')
            version = float(get_ngtd_version(ngtd_path))
            print(version)
            response = requests.get(link + f"{version}.xlsx", timeout=60)
            if response.status_code == 200:
                # TODO: Add logging of successful error code.
                print(response.status_code)
                ngtd_status = "NGTD version valid"
                continue
            elif response.status_code == 404:
                # TODO: Add logging of failed access
                # TODO: Add proper error handeling.  Might require learning how to raise custom errors.
                print(response.status_code)
                print("The current version of of the NGTD is nolonger valid."
                      "Attempting to download the updated version of the national genomic test directory"
                      )
                update_status, version_new = update_ngtd(version, file_directory, link)
                if update_status == "passed":
                    # os.remove(ngtd_path)
                    ngtd_status = f"NGTDv{version} nolonger valid. Successfully updated to NGTDv{version_new}"
                elif update_status == "failed":
                    update_failed = ("An updated version of the NGTD could not be found. To resolve this reach out to your "
                                            "Bioinformatics department"
                                            )
                    print(update_failed)
                    want_continue = ""
                    while want_continue == "":
                        want_continue = input("Do you want to continue with the existing version of the NGTD? [y/n]: ")
                        if want_continue.lower() == "n":
                            exit()
                        elif want_continue.lower() == "y":
                            ngtd_status = f"NGTDv{version} nolonger valid. Proceeding with old version test directory"
                            continue
                        else:
                            want_continue = input("Please enter y or n: ")
            elif response.status_code == 400:
                print("Error in establishing connecting to the internet")
                # TODO: add asking if to continue with old version.

            else:
                print("Function failed") # TODO This is temporary. Replace with something else.

    return ngtd_status
