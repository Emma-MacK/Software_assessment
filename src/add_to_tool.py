# importing modules
from ngtd_download import check_ngtd

# specifying location of NGTD file and saving all files to variable files.
# NGTD file available in repo is from version 5.1. of the genomic test
NGTD_DIRECTORY = 'test_directory_file'

# specifyng generic NGTD download link which can be modified by adding X.X.xlsx where X stands for a number
NGTD_LINK = "https://www.england.nhs.uk/wp-content/uploads/2018/08/Rare-and-inherited-disease-national-genomic-test-directory-version-"

print(check_ngtd(NGTD_DIRECTORY, NGTD_LINK))
