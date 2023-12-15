# import modules
import requests
import os
from datetime import datetime

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
file_path = 'bin'
age_in_days = get_file_age_in_days(file_path)

print(f"The file at {file_path} is approximately {age_in_days} days old.")


# # Uses request to download excel directly from NGTD website
# def ngtd_download(link):
#     response = requests.get(link)
#     version = link[-8:-5]
#     if response.status_code == 200:
#         with open(f'NGTDv{version}.xlsx', 'wb') as output:
#             output.write(response.content)
#     else:
#         print ('File not found error') #rudimentary error flag to be replaced by proper error handeling.

# # specifying excel download link of current download link
# download_link = ("https://www.england.nhs.uk/wp-content/uploads/2018/08/Rare-and-inherited-disease-national-genomic-test-directory-version-5.1.xlsx")

# # calling function and saving to variable xls
# xls = ngtd_download(download_link)

# # # removes file once the relevant data is pulled.
# # os.remove(f'NGTDv{version}.xls')
