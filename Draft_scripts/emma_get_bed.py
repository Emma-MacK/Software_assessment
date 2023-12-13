# script for me to get bed file
import requests
import json
import pandas

# ie "HGNC:4562"
# want the HGNC number
# add argument for flank value

def call_transcript_make_bed(HGNC_list, flank):
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
        except:
            print("An exception occurred connecting to variant validator")
            exit()

        # Keys in json ['current_name', 'current_symbol', 'hgnc', 'previous_symbol', 'requested_symbol', 'transcripts']
        print("JSON found")
        transcripts_list = json_dict["transcripts"]
        transcripts_dict= transcripts_list[0]

        # keys in subsection ['annotations', 'coding_end', 'coding_start', 'description', 'genomic_spans', 'length', 'reference', 'translation']

        # make bedfile header
        print("Making bed file for HGNC:" + str(HGNC))
        filename = HGNC + "_output.bed"
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
        json_name = HGNC + "_VV_output.json"
        # Writing to sample.json
        with open(json_name, "w") as outfile:
            outfile.write(json_object)


        # get start and end position for BED for each transcript
        genomic_spans_dict = transcripts_dict["genomic_spans"]
        for key in genomic_spans_dict:
            temp_dict = genomic_spans_dict[key]
            exon_list = temp_dict["exon_structure"]
            for item in exon_list:
                start = int(item["genomic_start"]) - flank
                end = int(item["genomic_end"]) + flank
                exon = item["exon_number"]
                # for each transcript reference, add to bed file
                with open(filename, 'a') as f:
                    f.write(chromosome + "\t" + str(start) + "\t" + str(end) + "\t" + str(key) + "\t" + "exon_" +str(exon) + "\n")

# HGNC will be called from raymond's section
HGNC = ["1100", "4562"]
# HGNC will be an argparse value (default 0)
flank = 25
call_transcript_make_bed(HGNC, flank)