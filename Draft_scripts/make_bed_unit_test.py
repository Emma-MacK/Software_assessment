# unit tests for function call_transcript_make_bed
import unittest
from unittest.mock import patch, mock_open, call

from functions import call_transcript_make_bed


# given correct input, expected to make a bed file and a json file
def test_expected_files():
    # given the input HGNC 4562, expect files 4562_output.bed and 4562_VV_output.json
    # if file names are changed, change tests
    HGNC = [4562]
    flank = 25
    genome_build = "GRCh37"
    transcript_set = "refseq"
    limited_transcripts = "mane_select"
    # set parameter so a mock command is run
    mock_open_files = mock_open()
    # anytiome open is called in functions, open mock files
    with patch("functions.open", mock_open_files, create=True):
        call_transcript_make_bed(HGNC, flank, genome_build, transcript_set, limited_transcripts)
    # check that while running call_transcript_make_bed, the files were interacted with
    mock_open_files.assert_any_call("4562_output.bed", "w")
    mock_open_files.assert_any_call("4562_VV_output.json", "w")

# output files have expected content
def test_file_content():
    # given the input HGNC 4562, expect files 4562_output.bed and 4562_VV_output.json
    # if file names are changed, change tests
    with open('test_expected_4562_output.bed', 'r') as file:
        # mock calls for header and content are seperate, remove header by spliting on strand
        expected_bed_data = str(file.read()).split("strand\n")[1]

    # each mock call will be for a seperate line
    expected_data_rows = expected_bed_data.split("\n")
    print(expected_data_rows)
    # each mock call will include \n at the end bar the last row, so re add
    for i in range(0,len(expected_data_rows) -1):
        expected_data_rows[i]= expected_data_rows[i] + "\n"

    # set variables for mock run
    HGNC = [4562]
    flank = 25
    genome_build = "GRCh37"
    transcript_set = "refseq"
    limited_transcripts = "mane_select"

    # set parameter so a file is not actually produced
    mock_open_files = mock_open()

    # anytiome open is called in functions, open mock files
    with patch("functions.open", mock_open_files, create=True):
        call_transcript_make_bed(HGNC, flank, genome_build, transcript_set, limited_transcripts)

    row_calls = mock_open_files().write.call_args_list
    # check that while running call_transcript_make_bed, the expected rows were added to the mock files
    # go by length so can ignore empty row at the end
    for row in range(0,len(expected_data_rows) -1):
        assert call(expected_data_rows[row]) in row_calls

# given incorrect input, expect informaticve error message
# output bedfile can be used by bedtools
# if api does not connect, fail informatively
# if HGNC id does not exist, fail informatively
# if url customisation is incorrect, fail informatively
# expect when given a HGNC ID to be given a specific json file
# given specific input, expecting specific output

# expected_files_test()