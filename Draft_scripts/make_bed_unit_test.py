# unit tests for function call_transcript_make_bed
import unittest
from unittest.mock import patch, mock_open

from functions import call_transcript_make_bed


# given correct input, expected to make a bed file and a json file
def test_expected_files():
    # given the input HGNC 4562, expect files 4562_output.bed and 4562_VV_output.json
    # if file names are changed, change tests
    HGNC = [4562]
    flank = 25
    # set parameter so a file is not actually produced
    mock_open_files = mock_open()
    # anytiome open is called in functions, open mock files
    with patch("functions.open", mock_open_files, create=True):
        call_transcript_make_bed(HGNC, flank)
    # check that while running call_transcript_make_bed, the files were interacted with
    mock_open_files.assert_any_call("4562_output.bed", "w")
    mock_open_files.assert_any_call("4562_VV_output.json", "w")

# output files have expected content
def test_file_content():

# given incorrect input, expect informaticve error message
# output bedfile can be used by bedtools
# if api does not connect, fail informatively
# if HGNC id does not exist, fail informatively
# if url customisation is incorrect, fail informatively
# expect when given a HGNC ID to be given a specific json file
# given specific input, expecting specific output

# expected_files_test()