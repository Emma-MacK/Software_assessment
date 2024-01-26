# unit tests for function call_transcript_make_bed
import unittest
import pytest
import json
from unittest.mock import patch, mock_open, call, Mock
from src.functions import call_transcript_make_bed

print("The following tests require VariantValidator to connect")
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
    with patch("src.functions.open", mock_open_files, create=True):
        call_transcript_make_bed(HGNC, flank, genome_build, transcript_set, limited_transcripts)
    # check that while running call_transcript_make_bed, the files were interacted with
    mock_open_files.assert_any_call("4562_output.bed", "w")
    mock_open_files.assert_any_call("4562_VV_output.json", "w")

# output files have expected content
def test_file_content():
    # given the input HGNC 4562, expect files 4562_output.bed and 4562_VV_output.json
    # if file names are changed, change tests
    with open('tests/test_expected_4562_output.bed', 'r') as file:
        # mock calls for header and content are seperate, remove header by spliting on strand
        expected_bed_data = str(file.read()).split("strand\n")[1]

    with open('tests/test_expected_4562_output.json', 'r') as file:
        expected_json = str(file.read())

    # each mock call will be for a seperate line
    expected_data_rows = expected_bed_data.split("\n")

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
    with patch("src.functions.open", mock_open_files, create=True):
        call_transcript_make_bed(HGNC, flank, genome_build, transcript_set, limited_transcripts)

    observed_calls = mock_open_files().write.call_args_list
    # check that while running call_transcript_make_bed, the expected rows were added to the mock files
    # go by length so can ignore empty row at the end
    for row in range(0,len(expected_data_rows) -1):
        assert call(expected_data_rows[row]) in observed_calls

    # Check the mock json was matches data from expected data
    assert call(expected_json) in observed_calls

# given incorrect input, expect informaticve error message
# output bedfile can be used by bedtools
# if api does not connect, fail informatively
# if HGNC id does not exist, fail informatively
# if url customisation is incorrect, fail informatively
# expect when given a HGNC ID to be given a specific json file
# given specific input, expecting specific output

# expected_files_test()

print("The following test should work even if variant validator is down")

@patch("functions.request.get")
def test_database_dict_and_bedfile(mock_requests_get):

    # load json file for mocking
    with open("tests/example_vv_get.json", "r") as file:
        json_content = json.load(file)

    # Assumes successful response from Variant Validator
    mock_response = Mock(status_code=200, content=json.dumps(json_content))
    mock_requests_get.return_value = mock_response

    # calling function with fixed inputs
    hgnc_list = ["4562"]
    flank = 25
    genome_build = "GRCh37"
    transcript_set = "refseq"
    limited_transcripts = "mane_select"

    result = call_transcript_make_bed(hgnc_list, flank, genome_build, transcript_set, limited_transcripts)

    # Assertions based on the expected behavior of your function
    assert isinstance(result, dict)

    expected_result = {
        "gene_name": "GRB2 related adaptor protein",
        "hgnc_id": "HGNC:4562",
        "hgnc_symbol": "GRAP",
        "refseq_id": "NM_006613.4",
        "ensembl_select": False,  # Ensure it's a boolean, not a string
        "mane_plus_clinical": False,  # Ensure it's a boolean, not a string
        "mane_select": True,  # Ensure it's a boolean, not a string
    }

    assert result == expected_result

    # Additional assertions based on your specific requirements

    # Check bedfile content
    with open("tests/make_bed_unit_test.py", "r") as bedfile:
        expected_bedfile_content = bedfile.read()

    assert expected_bedfile_content == """chromosome\tstart\tend\tname\tscore\tstrand
chr17\t18950137\t18950295\tNC_000017.10_GRAP_exon_1\t0\t-
chr17\t18945095\t18945242\tNC_000017.10_GRAP_exon_2\t0\t-
chr17\t18939246\t18939418\tNC_000017.10_GRAP_exon_3\t0\t-
chr17\t18927503\t18927721\tNC_000017.10_GRAP_exon_4\t0\t-
chr17\t18923944\t18925482\tNC_000017.10_GRAP_exon_5\t0\t-"""

if __name__ == '__main__':
    pytest.main()


