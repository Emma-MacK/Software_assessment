# script to hold functions
# TO DO: add error handling
import requests
import json
import pandas as pd
# Get information from test directory

def get_target_ngtd(testID):
    # get an excel into a pandas dataframe, getting specific columns
    # does the file exist? - incorparate Elena's functions when available
    xls = 'Rare-and-inherited-disease-national-genomic-test-directory-version-5.1.xlsx'
    test_directory_df = pd.read_excel(xls, 'R&ID indications', usecols="A:E", header=1)

    # get rows with a matching test code
    # does the testID exist in the test directory
    panel = test_directory_df.loc[test_directory_df['Clinical indication ID'] == testID]

    # print columns
    result_ngtd = panel['Target/Genes'].to_string(index=False)
    return result_ngtd

# get information from panel app

def get_target_panelapp(testID):

    # panelapp server
    # is there a way to set panel app version?
    server = "https://panelapp.genomicsengland.co.uk/api/v1"
    # insert R code
    ext = "/panels/" + testID

    # adds server and ext with id
    try:
        r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
        decoded = r.json()
        result_panelapp = repr(decoded)
        return result_panelapp

    except requests.exceptions.RequestException as e:
            # get details of exception
        print("An exception occurred connecting to PanelApp")
        raise SystemExit(e)
        exit()

# test user inputs
def check_testID(testID):
    in_test_directory=get_target_ngtd(testID)
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
                want_continue = input("Do you want to continue with a code not in the test directory? [y/n]: ")
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


def call_transcript_make_bed(HGNC_list, flank):
    # is there a way to do this without a set path?
    # Check HGNC list
    url_base = "https://rest.variantvalidator.org/VariantValidator/tools/gene2transcripts_v2/HGNC%3A"
    transcript_filter = "/mane_select/refseq/GRCh37"
    for HGNC in HGNC_list:

        full_url = url_base + str(HGNC)+ transcript_filter
        print("querying: " + full_url)
        try:
            r = requests.get(full_url, headers={ "content-type" : "application/json"})
            decoded = r.json()
            # print(repr(decoded))
            json_dict = decoded[0]
        except requests.exceptions.RequestException as e:
            # get details of exception
            print("An exception occurred connecting to variant validator")
            raise SystemExit(e)
            exit()

        # if the gene symbol does not exist returns {'error': 'Unable to recognise gene symbol NO DATA', 'requested_symbol': 'NO DATA'}
        # if json_dict["error"] exists print the error and exit
        if 'error' in json_dict:
            print("An error occured with variant validator")
            print(json_dict['error'])
            exit()


        # Keys in json ['current_name', 'current_symbol', 'hgnc', 'previous_symbol', 'requested_symbol', 'transcripts']
        print("JSON found")
        transcripts_dict = json_dict["transcripts"][0]
        # getting a section of the json returns a list with one element, [0] retrieves that element, making it a dict again
        # keys in transcripts_dict ['annotations', 'coding_end', 'coding_start', 'description', 'genomic_spans', 'length', 'reference', 'translation']

        # make bedfile header
        print("Making bed file for HGNC:" + str(HGNC))
        # set output location?
        # does file already exist
        filename = str(HGNC) + "_output.bed"
        with open(filename, 'w') as f:
            f.write("Chromosome\tstart\tend\tname\texon\n")

        # get chromosome for BED
        annotations_dict = transcripts_dict["annotations"]
        chromosome = str(annotations_dict["chromosome"])

        # get the info for database and write into json
        database_dict = {
            "refseq" : transcripts_dict["reference"],
            "ensembl_select" : str(annotations_dict["ensembl_select"]),
            "mane_plus_clinical" : str(annotations_dict["mane_plus_clinical"]),
            "mane_select" : str(annotations_dict["mane_select"])
        }
        json_object = json.dumps(database_dict, indent=4)
        json_name = str(HGNC) + "_VV_output.json"
        # Writing to sample.json
        with open(json_name, "w") as outfile:
            outfile.write(json_object)


        # get start and end position for BED for each transcript
        genomic_spans_dict = transcripts_dict["genomic_spans"]
        # get the keys, each corresponds to an exon
        for key in genomic_spans_dict:
            temp_dict = genomic_spans_dict[key]
            exon_list = temp_dict["exon_structure"]
            for item in exon_list:
                # get the transcript positions and adjust with the flank
                start = int(item["genomic_start"]) - flank
                end = int(item["genomic_end"]) + flank
                # label each exon
                exon = item["exon_number"]
                # for each transcript reference, add to bed file
                with open(filename, 'a') as f:
                    f.write(chromosome + "\t" + str(start) + "\t" + str(end) + "\t" + str(key) + "\t" + "exon_" +str(exon) + "\n")
