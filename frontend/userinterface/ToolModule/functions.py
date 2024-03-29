# script to hold functions
# TO DO: add error handling
import requests
import json
import pandas as pd


def get_target_ngtd(testID):
    """Get the genes in a panel from the NGTD for an testID

    Args:
        testID (str): The ID of a specific test in the format Rxx

    Returns:
        result_ngtd: A series (column from a pandas dataframe)
        of the target genesfor a given test ID
    """

    # trun xlsx database into pandas dataframe
    xls = ('Rare-and-inherited-disease-national'
           '-genomic-test-directory-version-5.1.xlsx')
    test_directory_df = pd.read_excel(xls, 'R&ID indications',
                                      usecols="A:E", header=1)

    # get rows with a matching test code
    # does the testID exist in the test directory
    panel = test_directory_df.loc[test_directory_df['Clinical \
                                                    indication ID'] == testID]

    # print columns
    result_ngtd = panel['Target/Genes'].to_string(index=False)
    return result_ngtd


def get_target_panelapp(testID):

    """ Get panel information from panel app for the given test ID

    Args:
        testID (str): The ID of a specific test in the format Rxx

    Raises:
        SystemExit: Unable to connect to panel app

    Returns:
        result_panelapp: The json file returned from querying panelapp,
        holds information for the given R code
    """

    server = "https://panelapp.genomicsengland.co.uk/api/v1"
    # insert R code
    ext = "/panels/" + testID

    # use try and except to handle errors connecting to panelapp
    try:
        r = requests.get(server+ext,
                         headers={"Content-Type": "application/json"})
        decoded = r.json()
        result_panelapp = repr(decoded)
        return result_panelapp

    except requests.exceptions.RequestException as e:
        # get details of exception
        print("An exception occurred connecting to PanelApp")
        raise SystemExit(e)
        exit()


def check_testID(testID):
    """Test the given R code to ensure it is in the correct format
      and check it exists in the test directory

    Args:
        testID (str): The ID of a specific test in the format Rxx

    Returns:
        result (str): A printed string informing user of an incorrect format,
        or prompt the user to continue if the R code
        does not exist in the test directory
    """
    in_test_directory = get_target_ngtd(testID)
    # check the ID begins with R
    if testID[:1] != "R":
        result = "invalid R code format"
    # elif does not exist in the test directory
    else:
        if in_test_directory == "Series([], )":
            want_continue = "Please enter y or n"
            result = "R does not exist in test directory"
            print(result)
            # ask user if they want to continue
            while want_continue == "Please enter y or n":
                want_continue = input("Do you want to continue with \
                                      a code not in the test \
                                      directory? [y/n]: ")
                if want_continue == "y":
                    print("Proceeding with " + testID)
                elif want_continue == "n":
                    exit()
                else:
                    want_continue = "Please enter y or n"
                    print(want_continue)
        else:
            result = "R code found in test directory: \n" + in_test_directory
    return result


def call_transcript_make_bed(HGNC_list, flank, genome_build,
                             transcript_set, limited_transcripts):
    """A function that uses the HGNC ID from the panelapp json
    to gather gene info from variant validator's gene to transcript tool
    Builds a bed file and a json file for use in our database

    Args:
        HGNC_list (str): A gene ID to query in variant validator
        flank (int): The number of bases add as a flank to regions in bed file
        genome_build (str): The genome build to use. GRCh37, GRCh38, or all
        transcript_set (str): the transcript source to use.
                              refseq, ensembl, or all
        limited_transcripts (str): The transcripts to use.
                                   mane_select, mane, select
    """

    # build the url for connecting to variant validator
    url_base = ("https://rest.variantvalidator.org/"
                "VariantValidator/tools/gene2transcripts_v2/HGNC%3A")
    transcript_filter = ("/"
                         + limited_transcripts
                         + "/"
                         + transcript_set
                         + "/"
                         + genome_build)

    # make empty bed file
    print("Making bed file for gene list:" + str(HGNC_list))
    concat_filename = "panel_output.bed"
    with open(concat_filename, 'w') as f:
        f.write("chrom\tchromStart\tchromEnd\tname\tscore\tstrand\n")

    # Check HGNC list
    for HGNC in HGNC_list:
        full_url = url_base + str(HGNC) + transcript_filter
        print("querying: " + full_url)
        try:
            r = requests.get(full_url,
                             headers={"content-type": "application/json"})
            decoded = r.json()
            # print(repr(decoded))
            json_dict = decoded[0]
        except requests.exceptions.RequestException as e:
            print("An exception occurred connecting to variant validator")
            raise SystemExit(e) from e
            # exit()

        # if the gene symbol does not exist returns {'error':
        # 'Unable to recognise gene symbol NO DATA',
        #  'requested_symbol': 'NO DATA'}
        # if json_dict["error"] exists print the error and exit
        if 'error' in json_dict:
            print("An error occured with variant validator: \
                  No data available for this request")
            print(json_dict['error'])
            exit()

        # Keys in json ['current_name', 'current_symbol', 'hgnc',
        # 'previous_symbol', 'requested_symbol', 'transcripts']
        print("JSON found")
        transcripts_list = json_dict["transcripts"]

        # case where entry (using genome_build = "GRCh38",
        # transcript_set = "ensembl", limited_transcripts = "select")
        # produced empty "transcripts" dict in json.
        # Set up code to return informative message
        # empty dicts == false in python

        if not transcripts_list:
            print(json_dict)
            print("No transcript information available, \
                  cannot produce bed file for this request")
            exit()

        transcripts_dict = transcripts_list[0]

        # keys in subsection ['annotations', 'coding_end',
        # 'coding_start', 'description', 'genomic_spans',
        # 'length', 'reference', 'translation']
        # print(json_dict)

        # get chromosome for BED
        annotations_dict = transcripts_dict["annotations"]
        chromosome = "chr"+str(annotations_dict["chromosome"])

        # get the info for database and write into json
        database_dict = {
            "gene_name": json_dict["current_name"],
            "hgnc_ID": json_dict["hgnc"],
            "hgnc_symbol": json_dict["current_symbol"],
            "refseq_id": transcripts_dict["reference"],
            "ensembl_select": str(annotations_dict["ensembl_select"]),
            "mane_plus_clinical": str(annotations_dict["mane_plus_clinical"]),
            "mane_select": str(annotations_dict["mane_select"])
        }
        json_object = json.dumps(database_dict, indent=4)
        json_name = str(HGNC) + "_VV_output.json"
        # Writing to sample.json
        with open(json_name, "w") as outfile:
            outfile.write(json_object)

        # make bedfile header
        print("Making bed file for HGNC:" + str(HGNC))
        filename = str(HGNC) + "_output.bed"
        with open(filename, 'w') as f:
            f.write("chromosome\tstart\tend\tname\tscore\tstrand\n")

        # build bed file
        genomic_spans_dict = transcripts_dict["genomic_spans"]

        # get start and end position for BED for each transcript
        for key in genomic_spans_dict:
            temp_dict = genomic_spans_dict[key]
            exon_list = temp_dict["exon_structure"]

        # get strand for bed, held in orientation. 1 = +, -1 = -
            if temp_dict["orientation"] == 1:
                sense = "+"
            elif temp_dict["orientation"] == -1:
                sense = "-"
            else:
                sense = "NA"
            for item in exon_list:
                start = int(item["genomic_start"]) - flank
                end = int(item["genomic_end"]) + flank
                label = (str(key)
                         + "_"
                         + json_dict["current_symbol"]
                         + "_exon_"
                         + str(item["exon_number"]))
                # for each transcript reference, add to bed file
                with open(filename, 'a') as f:
                    f.write(chromosome
                            + "\t"
                            + str(start)
                            + "\t"
                            + str(end)
                            + "\t"
                            + label
                            + "\t"
                            + str(0)
                            + "\t"
                            + sense
                            + "\n")
                # add to big bed file
                with open(concat_filename, 'a') as f:
                    f.write(chromosome
                            + "\t"
                            + str(start)
                            + "\t"
                            + str(end)
                            + "\t"
                            + label
                            + "\t"
                            + str(0)
                            + "\t"
                            + sense
                            + "\n")
