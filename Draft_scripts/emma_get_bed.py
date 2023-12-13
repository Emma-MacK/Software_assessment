# script for me to get bed file

from functions import call_transcript_make_bed

# ie "HGNC:4562"
# want the HGNC number
# add argument for flank value


# HGNC will be called from raymond's section
HGNC = [123, "4562"]
# HGNC will be an argparse value (default 0)
flank = 25
call_transcript_make_bed(HGNC, flank)