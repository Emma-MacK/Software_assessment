# script for me to get bed file
import requests
import json
import pandas

# get HGNC id from JSON, API variant validator genes to transcripts, get bed files?
# ie "HGNC:4562"
# want the HGNC number
# Merged into one bed for multiple gene beds?


url = "https://rest.variantvalidator.org/VariantValidator/tools/gene2transcripts_v2/HGNC%3"


# TO DO
HGNC = "id go here, from raymond's code"

# can personalise filtering later?
transcript_filter = "/mane_select/refseq/GRCh37"

# build full request

full_url = url + HGNC + transcript_filter

#try:
#  r = requests.get("https://rest.variantvalidator.org/VariantValidator/tools/gene2transcripts_v2/HGNC%3A4562/mane_select/refseq/GRCh37", headers={ "content-type" : "application/json"})
#  decoded = r.json()
#  print(repr(decoded))
#except:
#  print("An exception occurred")

# json is actually in a list?
with open('Draft_scripts/test.json') as f:
    json_dict = json.load(f)[0]

# Keys in json ['current_name', 'current_symbol', 'hgnc', 'previous_symbol', 'requested_symbol', 'transcripts']

transcripts_list = json_dict["transcripts"]
transcripts_dict= transcripts_list[0]

# keys in subsection ['annotations', 'coding_end', 'coding_start', 'description', 'genomic_spans', 'length', 'reference', 'translation']
# get the Refseq ID for database
RefSeq = transcripts_dict["reference"]

# bedfile header
with open('output.bed', 'w') as f:
    f.write("Chromosome\tstart\tend\tname\n")

# get chromosome for BED
annotations_dict = transcripts_dict["annotations"]
chromosome = str(annotations_dict["chromosome"])

# get start and end position for BED for each transcript
genomic_spans_dict = transcripts_dict["genomic_spans"]
for key in genomic_spans_dict:
    temp_dict = genomic_spans_dict[key]
    start = temp_dict["start_position"]
    end = temp_dict["end_position"]

    # for each transcript reference, add to bed file
    with open('output.bed', 'a') as f:
        f.write(chromosome + "\t" + str(start) + "\t" + str(end) + "\t" + str(key) + "\n")
