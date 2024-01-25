"""
bedfile_to_database.py

This module allows bedfile data to be pushed to the database
from existing bedfiles assuming they follow the naming
convention defined below.

TODO: Module assumes the database is located in the directory
from which you are executing this module.
"""

import os
import fnmatch
import re

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from panel_db_2 import Base, Bedfile

# create an empty database
engine = create_engine("sqlite:///panel_db.db", echo=True)

# create an empty database with the structure outlined above
Base.metadata.create_all(bind=engine)

# create session
Session = sessionmaker(bind=engine)
session = Session()

# specifying data types for Pandas DataFrame
column_types = {
    "hgnc_id": str,
    "refseq_id": str,
    "chromosome": str,
    "start": int,
    "end": int,
    "name": str,
    "score": int,
    "strand": str
}

# specifying path to json files
# TODO: Update file path as necessary
BEDFILES_FILE_PATH = "tests/bedfiles"

#getting list of bedfile
files = os.listdir(BEDFILES_FILE_PATH)
FILE_NAME_PATTERN = '*.bed'
matching_files = fnmatch.filter(files, FILE_NAME_PATTERN)
print(matching_files)

for file in matching_files:
    file_path = os.path.join(BEDFILES_FILE_PATH, file)
    # reading bedfile into a DataFrame
    bed_df = pd.read_csv(file_path,
                     sep="\t",
                     comment="#",
                     dtype=column_types
                         )
    print(bed_df)

    #converting list to string
    file_name = str(file_path)

    #defining file name pattern
    # TODO: Update patten if needed
    string_pattern = re.compile(r'(\d+)_(NM_\d+\.\d+)\.bed')

    #parsing HGNC id and Refseq from file name
    name_elements = string_pattern.search(file_name)
    hgnc_id = name_elements.group(1)
    refseq_id = name_elements.group(2)
    print(hgnc_id)
    print(refseq_id)

    # adding data to the dataframe
    new_rows_df = pd.DataFrame({
        "hgnc_id": [hgnc_id] * len(bed_df),
        "refseq_id": [refseq_id] * len(bed_df)
    })
    database_df = pd.concat([bed_df, new_rows_df], axis=1)

    print(database_df)

    # Insert data into bedfile database
    for index, row in database_df.iterrows():
        feature = Bedfile(
            chromosome=row["chromosome"],
            start=row["start"],
            end=row["end"],
            name=row["name"],
            score=row["score"],
            strand=row["strand"],
            hgnc_id=row["hgnc_id"],
            refseq_id=row["refseq_id"]
            )

        session.add(feature)

    # commit
    session.commit()
