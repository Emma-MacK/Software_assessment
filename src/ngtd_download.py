# import modules
import requests
import os

# Uses request to download excel directly from NGTD website
def ngtd_download(link):
    response = requests.get(link)
    if response.status_code == 200:
        with open('NGTD.xls', 'wb') as output:
            output.write(response.content)
    else:
        print ('File not found error') #rudimentary error flag to be replaced by proper error handeling.

# specifying excel download link of current download link
download_link = ("https://www.england.nhs.uk/wp-content/uploads/2018/08/Rare-and-inherited-disease-national-genomic-test-directory-version-5.1.xlsx")

# calling function and saving to variable xls
xls = ngtd_download(download_link)

# removes file once the relevant data is pulled.
os.remove('NGTD.xls')

