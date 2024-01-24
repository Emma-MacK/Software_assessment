# unit tests for function call_transcript_make_bed
import unittest
from unittest.mock import patch, mock_open, call
from src.functions import get_hgncIDs

# the test case is R208. The json produced from panel app is present
# it is expected when given the panel app json for 208
# get_hgncIDs will return the following ids

expected_ids = ['1100', '1101', '16627', '26144', '9820', '9823']

# given expected input, do we get expected output
def test_expected_ids():
    with open('tests/test_panelapp_call.json', 'r') as file:
        expected_json = str(file.read())
    assert get_hgncIDs(expected_json) == expected_ids