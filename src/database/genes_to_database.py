"""
genes_to_database.py

This module allows gene data from panels to be pushed
to the database from existing json file with the following structure

[
    {
        "panel_id_v": "2.11",
        "gene_name": "acid phosphatase 2, lysosomal",
        "hgnc_id": "HGNC:123",
        "hgnc_symbol": "ACP2",
        "omim_no": "607585",
        "refseq_id": "NM_001610.4",
        "ensembl_select": false,
        "mane_plus_clinical": false,
        "mane_select": true
    }
]

TODO: Module assumes the database is located in the directory
from which you are executing this module.
"""

import json
import os
import fnmatch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from panel_db_2 import Base, Genes

# create an empty database
engine = create_engine("sqlite:///panel_db.db", echo=True)

# create an empty database with the structure outlined above
Base.metadata.create_all(bind=engine)

# create session
Session = sessionmaker(bind=engine)
session = Session()

# specifying path to json files
# TODO: Update file path as necessary
json_files_path = "tests/gene_info_jsons"

# getting list of json files
files = os.listdir(json_files_path)
file_name_pattern = '*.json'
matching_files = fnmatch.filter(files, file_name_pattern)
print(matching_files)


for file in matching_files:
    file_path = os.path.join(json_files_path, file)
    with open(file_path, "r") as json_file:
        data = json.load(json_file)

# add data from json into Genes table
for item in data:

    new_record = Genes(**item)
    session.add(new_record)

session.commit()
