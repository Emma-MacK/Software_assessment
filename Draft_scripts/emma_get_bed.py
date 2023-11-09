# script for me to get bed file
import requests


# get HGNC id from JSON, API variant validator genes to transcripts, get bed files?
# ie "HGNC:4562"
# want the HGNC number
# Merged into one bed for multiple gene beds?



r = requests.get("https://rest.variantvalidator.org/VariantValidator/tools/gene2transcripts_v2/HGNC%3A4562/mane_select/RefSeq/all", headers={ "content-type" : "application/json"})

#returns data
decoded = r.json()
print(repr(decoded))