# script to hold functions
# TO DO: add error handling
import os
import fnmatch
from math import floor
from datetime import datetime
import json
import requests
import logging
import logging.config
import time
import pandas as pd

# setting the logging.Formatter to use GMT time as default.
# Guarantees that the log file always reflects UK local time
logging.Formatter.converter = time.gmtime

# loading logging configuration from logging.conf
# logging will log to the same rotating file handler as tool_v2.py logging
logging.config.fileConfig('config/logging.conf')

# create/get logger
logger = logging.getLogger()

# setting the logging.Formatter to use GMT time as default.
# Guarantees that the log file always reflects UK local time
logging.Formatter.converter = time.gmtime

# loading logging configuration from logging.conf
# logging will log to the same rotating file handler as tool_v2.py logging
logging.config.fileConfig('config/logging.conf')

# create/get logger
logger = logging.getLogger()


def get_target_ngtd(testID, file_directory, version):
    """Get the genes in a panel from the NGTD for an testID

    Args:
    - testID (str): The ID of a specific test in the format Rxx
    - file_directory: The relative OR absolute path to the directory
    where the NGTD file is saved.
    - version: The version number of the NGTD

    Returns:
        - result_ngtd: A series (column from a pandas dataframe)
        of the target genes for a given test ID
    """
    NGTD_file = os.path.join(file_directory, f"NGTDv{version}.xlsx")
    test_directory_df = pd.read_excel(NGTD_file, 'R&ID indications', usecols="A:E", header=1)


    # get rows with a matching test code
    # does the testID exist in the test directory
    panel = test_directory_df.loc[
        test_directory_df['Clinical indication ID'] == testID
        ]

    # print columns
    result_ngtd = panel['Target/Genes'].to_string(index=False)
    return result_ngtd

def get_target_panelapp(testID):

    """ Get panel information from panel app for the given test ID

    Args:
        - testID (str): The ID of a specific test in the format Rxx

    Raises:
        - SystemExit: Unable to connect to panel app

    Returns:
        - result_panelapp: The json file returned from querying panelapp,
        holds information for the given R code
    """

    server = "https://panelapp.genomicsengland.co.uk/api/v1"
    # insert R code
    ext = "/panels/" + testID

    # use try and except to handle errors connecting to panelapp
    try:
        logging.info("Attempting to pull data from PanelApp Api")
        r = requests.get(server+ext, headers={"Content-Type" : "application/json"}, timeout=120) # TODO Sentence to long for PEP8
        decoded = r.json()
        result_panelapp = json.dumps(decoded, indent = 2)
        return result_panelapp

    except requests.exceptions.RequestException as e:
        # get details of exception
        print("An exception occurred connecting to PanelApp")
        logging.error("Unable to connect to Panel App. System Exit raised") # TODO Sentence to long for PEP8
        raise SystemExit(e) from e
        # exit()


def get_hgncIDs(result_panelapp):

    """Take the result of the panel app query and extract HGNC IDs

    Args:
        result_panelapp (str): A json file in string format, returned from querying panel app

    Returns:
        all_IDs (list): A list of HGNC ids for the genes in a panel
    """
    panel_json = json.loads(result_panelapp)

    # some cases return "{'detail': 'Not found.'}" indicating not in panel app
    # example; R24 goes to FGFR3 c.1138, looking for a specific mutations
    if 'detail' in panel_json:
        if panel_json['detail'] == "Not found.":
            print("This R code does not have an associated panel")
            print("This R code may not call for an NGS test")
            exit()

    gene_info = panel_json["genes"]
    all_IDs = []
    # there are multiple genes in the list, loop over to get all HGNC ids
    for i in range(1,len(gene_info)):
        gene_info_item = gene_info[i]
        gene_data = gene_info_item['gene_data']
        hgnc_id = gene_data["hgnc_id"]
        all_IDs.append(hgnc_id)

    all_IDs = ' '.join(all_IDs).replace('HGNC:','').split()

    # check if list is empty
    if len(all_IDs) == 0:
        print("No gene IDs found for this ID")
        exit()
    return all_IDs

def check_testID(testID, file_directory, version):
    """Test the given R code to ensure it is in the correct format
      and check it exists in the test directory

    Args:
    - testID (str): The ID of a specific test in the format Rxx
    - file_directory: The relative OR absolute path to the directory
    where the NGTD file is saved.
    - version: The version number of the NGTD

    Returns:
        - result (str): A printed string informing user of an incorrect
        format, or prompt the user to continue if the R code does not
        exist in the test directory
    """
    in_test_directory=get_target_ngtd(testID, file_directory, version)
    # check the ID begins with R
    if testID[:1] != "R":
        result = "invalid R code format"
    # elif does not exist in the test directory
    else:
        if in_test_directory == "Series([], )":
            print("Test ID not found within the test directory")
            logging.info("Test ID not found within the test directory")
            # ask user if they want to continue
            want_continue = "Please enter y or n"
            while want_continue == "Please enter y or n":
                want_continue = input("Do you want to continue with a code not in the test directory? [y/n]: ").lower()
                if want_continue == "y":
                    result = f"Proceeding with test ID {testID}"
                    logging.warning("User proceeding with non-NGTD panel")
                    print(result)
                elif want_continue == "n":
                    logging.info("User requested system exit")
                    exit()
                else:
                    want_continue = input("Please enter y or n").lower()
                    print(want_continue)
        else:
            result = "Test ID found in the national genomic test directory"
    return result

def get_file_age_in_days(file_path):
    """Gets the age of a file in days

    Args:
    - file_path: The relative OR absolute path to the file location

    Returns:
    - age_in_days: variable holding the age of the file as an int.

    """
    # Get the file's modification timestamp
    timestamp = os.path.getmtime(file_path)

    # Convert the timestamp to a datetime object
    modification_time = datetime.fromtimestamp(timestamp)

    # Get the current time
    current_time = datetime.now()

    # Calculate the age of the file in terms of months
    age_in_days = (current_time - modification_time).days
    return age_in_days

def get_ngtd_version(file_path):
    """Parses the NGTD version number from within the file.

    Args:
    - file_path: The relative OR absolute path to the file location

    Returns:
    - version: Returns the version number as a string output
    """
    # Loading Columns A of file into a Dataframe
    test_directory_df = pd.read_excel(file_path, 'R&ID indications', usecols="A", header=0)

    #extracting and cleaning data from first row
    test_directory_header = str(test_directory_df.iloc[0])
    first_split = test_directory_header.split(",")
    section_of_header = first_split[1]
    section_of_header_clean = section_of_header.strip( )
    second_split = section_of_header_clean.split(" ")
    section_of_header = second_split[0]
    section_of_header_clean = section_of_header.strip( )
    version = section_of_header_clean[1:]

    # TODO: attempt to convert to float as test to see if correctly parsed.

    return version

def update_ngtd(version, file_directory, link, perform_file_write=True):
    """Makes three attempts to obtain an updated version of the NGTD"
    1. Minor update (+ 0.1)
    2. Major update (+ 1.0) as float
    3. Major update (+1) as int

    Args:
    - version: The version number of the NGTD
    - file_directory: The relative OR absolute path to the directory
    where the updated file should be saved
    - link: The link to where the NGTD directory is sourced. This should
    always be the constant variable "NGTD" specified in tool_v2.py
    - perform_file_write: Set to <true> as default. Overriding this to
    <false> results in the updated test directory not being written to
    an excel file.

    Returns:
    - update_status: Confirmation about whether the update succeeded or
    failed
    - version_new: The version number of the new NGTD. If the update
    was unsuccessful this variable contains just and empty string

    """
    # NOTE: Had previously tried to do this with a try block but couldn't think through the logic.
    # TODO: Remove print statements and replace with logging
    # Some elements of this function are bit repetetive and could maybe we streamlined into another function

    # update version number assuming a minor change has been made
    print(version)

    version_new = round(float(version) + 0.1, 1)
    print(version_new)
    update_status = ""

    # Use request to try and obtain a copy of the file with an updated version number.
    response = requests.get(link + f"{version_new}.xlsx", timeout=60)
    # TODO: Add logging to record the version number tried.
    # TODO: Add error handeling for the timeout
    if response.status_code == 200:
        print(response.status_code)
        # TODO: Add logging to record response code and that this means file is still current.
        if perform_file_write:
            path_new_file = os.path.join(file_directory, f"NGTDv{version_new}.xlsx")
            with open(path_new_file, 'wb') as output:
                output.write(response.content)
        update_status = "passed"

    # Try to see if a copy of the file can be obtained assuming a major update has been made.
    elif response.status_code == 404:
        print(response.status_code)
        version_new = floor(float(version)) + 1.0
        # TODO: Add logging to record the version number tried.
        print(version_new)
        response = requests.get(link + f"{version_new}.xlsx", timeout=60)
        if response.status_code == 200:
            # TODO: Add logging to record response code. Do this throughout this function
            if perform_file_write:
                path_new_file = os.path.join(file_directory, f"NGTDv{version_new}.xlsx")
                with open(path_new_file, 'wb') as output:
                    output.write(response.content)
            update_status = "passed"
                # TODO: Check where the output file is being written to.
        elif response.status_code == 404:
            version_new = int(version_new)
            print(version_new)
            response = requests.get(link +f"{version_new}.xlsx", timeout=60)
            if response.status_code == 200:
                print(response.status_code)
                if perform_file_write:
                    path_new_file = os.path.join(file_directory, f"NGTDv{version_new}.xlsx")
                    with open(path_new_file, 'wb') as output:
                        output.write(response.content)
                update_status = "passed"
            else:
                update_status = "failed"
                version_new = ""

    return update_status, version_new # TODO: Test if this actually returns back to the else statement or not.

    # Asks the user whether to proceed with the existing version of the NGTD if it fails to get an updated version.
    # else:

    # return # TODO: Does this successfully exit the function and move on?

def check_ngtd(file_directory, link):
    """Checks the age and validity of the NGTD version, attempting to
    update to a more recent version if necessary.
    N.B. Where unable to update the version user will be given the
    option to proceed with existing version

    Args:
    - file_directory: The relative OR absolute path to the directory
    where the NGTD file is saved.
    - link: The link to where the NGTD directory is sourced. This should
    always be the constant variable "NGTD" specified in tool_v2.py

    Returns:
    - ngtd_status: Confirmation about the status of the NGTD
    - version: The confirmed version of the NGTD
    """

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
        version = (get_ngtd_version(ngtd_path))
        print(version)
        # TODO: For loop might be excessive since we only expect one file. Also what happens if there is more than one file?
        if get_file_age_in_days(ngtd_path) < 30:
            # TODO: Add logging of file age
            ngtd_status = "NGTD file younger than 30 days"
            continue
        elif get_file_age_in_days(ngtd_path) >= 30:
            # TODO: Add logging of file age
            print('File is older than 30 days old')
            try:
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
                        os.remove(ngtd_path) # removing old NGTD version
                        ngtd_status = f"NGTDv{version} nolonger valid. Successfully updated to NGTDv{version_new}"
                        version = version_new
                    elif update_status == "failed":
                        update_failed = ("An updated version of the NGTD could not be found. To resolve this reach out to your "
                                                "Bioinformatics department"
                                                )
                        print(update_failed)
                        want_continue = ""
                        while want_continue == "":
                            want_continue = input("Do you want to continue with the existing version of the NGTD? [y/n]: ").lower()
                            if want_continue == "n":
                                exit()
                            elif want_continue == "y":
                                ngtd_status = f"NGTDv{version} nolonger valid. Proceeding with old version test directory"
                                continue
                            else:
                                want_continue = input("Please enter y or n: ").lower()
            except requests.exceptions.RequestException as e:
                # get details of exception
                print("An exception occurred connecting to national genomic test directory")
                want_continue = ""
                while want_continue == "":
                            want_continue = input("Do you want to continue with the existing version of the NGTD? [y/n]: ").lower()
                            if want_continue == "n":
                                raise SystemExit(e)
                            elif want_continue == "y":
                                ngtd_status = f"Proceeding with existing version version test directory: {version}"
                                break
                            else:
                                want_continue = input("Please enter y or n: ").lower()
                # TODO add logging

    return ngtd_status, version

def call_transcript_make_bed(hgnc_list, flank, genome_build,
                             transcript_set, limited_transcripts):
    """A function that uses the HGNC ID from the panelapp json
    to gather gene info from variant validator's gene to transcript tool
    Builds a bed file and a json file for use in our database

    Args:
        - HGNC_list (str): A gene ID to query in variant validator
        flank (int): The number of bases add as a flank to regions in
        bed file
        - genome_build (str): The genome build to use. GRCh37, GRCh38,
        or all
        - transcript_set (str): the transcript source to use. refseq,
        ensembl, or all
        - limited_transcripts (str): The transcript to use. mane_select,
        mane, select
    """

    # get date and time for savinf files
    date_of_running = datetime.now()
    dt_string = date_of_running.strftime("%d%m%Y_%H%M%S")

    # build the url for connecting to variant validator
    url_base = ("https://rest.variantvalidator.org/VariantValidator/tools/gene2transcripts_v2/HGNC%3A/") # TODO to long for PEP8 standards
    transcript_filter = "/" + limited_transcripts + "/" + transcript_set + "/" + genome_build # TODO to long for PEP8 standards

    os.mkdir("output/" + dt_string)
    # make empty bed file
    print("Making bed file for gene list:" + str(hgnc_list))
    concat_filename = "output/" + dt_string + "/panel_output.bed"
    with open(concat_filename, 'w') as f:
        f.write("chrom\tchromStart\tchromEnd\tname\tscore\tstrand\n")

    # Check HGNC list
    for hgnc in hgnc_list:
        full_url = url_base + str(hgnc)+ transcript_filter
        print("querying: " + full_url)
        logging.info("Querying: %s", full_url)
        try:

            r = requests.get(full_url,
                             headers={ "content-type" : "application/json"},
                             timeout=120) # TODO to long for PEP8 standards.
            decoded = r.json()
            # print(repr(decoded))

            # check if variantvalidator is down
            # a dict is returned, so no error produced by get request
            if 'message' in decoded:
                print(decoded['message'])
                print("Variant Validator may be experiencing internal server errors")
                exit()
            json_dict = decoded[0]
        except requests.exceptions.RequestException as e:
            print("An exception occurred connecting to variant validator")
            logging.error("Unable to connect to VariantValidator,"
                          " System exit raised")
            raise SystemExit(e) from e
            # exit()

        # if the gene symbol does not exist returns
        # {'error': 'Unable to recognise gene symbol NO DATA', 'requested_symbol': 'NO DATA'}
        # if json_dict["error"] exists print the error and exit
        if 'error' in json_dict:
            print("An error occured connecting to variant validator: "
                  "No data available for this request")
            print(json_dict['error'])
            exit()

        # Keys in json ['current_name', 'current_symbol', 'hgnc',
            # 'previous_symbol', 'requested_symbol', 'transcripts']
        # print("JSON found")
        logging.info("Json successfully returned")
        transcripts_list = json_dict["transcripts"]

        # case where entry (using genome_build = "GRCh38",
        # transcript_set = "ensembl", limited_transcripts = "select")
        # produced empty "transcripts" dict in json. Set up code to return informative message
        # empty dicts == false in python

        if not transcripts_list:
            print(json_dict)
            print("No transcript information available, cannot produce bed "
                  "file for this request")
            logging.error("Transcript information unavailable. "
                          "Unable to produce bed file. System exit raised")
            exit()

        transcripts_dict = transcripts_list[0]


        # keys in subsection ['annotations', 'coding_end', 'coding_start', 'description', 'genomic_spans', 'length', 'reference', 'translation']
        # print(json_dict)

        # get chromosome for BED
        annotations_dict = transcripts_dict["annotations"]
        chromosome = "chr"+str(annotations_dict["chromosome"])

        # get refseq id for bedfile name
        refseq_id = transcripts_dict["reference"]

        # get the info for database and write into json
        database_dict = {
            "gene_name": json_dict["current_name"],
            "hgnc_ID": json_dict["hgnc"],
            "hgnc_symbol": json_dict["current_symbol"],
            "refseq_id" : transcripts_dict["reference"],
            "ensembl_select" : str(annotations_dict["ensembl_select"]),
            "mane_plus_clinical" : str(annotations_dict["mane_plus_clinical"]),
            "mane_select" : str(annotations_dict["mane_select"])
        }
        json_object = json.dumps(database_dict, indent=4)
        json_name = "output/" + dt_string + "/" + str(hgnc) + "_VV_output.json"
        # Writing to sample.json
        with open(json_name, "w") as outfile:
            outfile.write(json_object)
        logging.info("json containing data for database entry created")

        # make bedfile header
        print("Making bed file for HGNC:" + str(hgnc))
        filename = "output/" + dt_string + "/" + str(hgnc) + str(refseq_id) + "_output.bed"
        with open(filename, 'w') as f:
            f.write("chromosome\tstart\tend\tname\tscore\tstrand\n")

        # build bed file
        genomic_spans_dict = transcripts_dict["genomic_spans"]

        # get start and end position for BED for each transcript
        for key in genomic_spans_dict:
            temp_dict = genomic_spans_dict[key]
            exon_list = temp_dict["exon_structure"]
            logging.debug("")

        # get strand for bed, held in orientation. 1 = +, -1 = -
            if temp_dict["orientation"] == 1:
                sense = "+"
            elif temp_dict["orientation"] ==-1:
                sense = "-"
            else:
                sense = "NA"
            for item in exon_list:
                start = int(item["genomic_start"]) - flank
                end = int(item["genomic_end"]) + flank
                label = str(key)+ "_" + json_dict["current_symbol"] +"_exon_"+ str(item["exon_number"])
                # for each transcript reference, add to bed file
                with open(filename, 'a') as f:
                    f.write(chromosome + "\t" + str(start) + "\t" + str(end) + "\t" + label + "\t" + str(0) +"\t" + sense + "\n")
                # add to big bed file
                with open(concat_filename, 'a') as f:
                    f.write(chromosome + "\t" + str(start) + "\t" + str(end) + "\t" + label + "\t" + str(0) +"\t" + sense + "\n")
        logging.info("Bedfiles created. %sbp flanking region used", flank)
