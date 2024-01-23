import pandas as pd
import json

from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, Boolean, insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
import pandas as pd

Base = declarative_base()

# creating bedfile table

class Bedfile(Base):
    __tablename__ = "bedfile"

    entry_id = Column("entry_id", Integer, primary_key=True, autoincrement=True)
    gene_name = Column("Gene Name", String)
    hgnc_id = Column("HGNC IDm", Integer) # TODO add foreign key when integrated with rest of database
    chromosome = Column("Chromosome", String)
    start = Column("Start", Integer)
    end = Column("End", Integer)
    name = Column ("Name", String)
    score = Column ("Score", Integer)
    strand = Column ("Strand Direction", String)

# create an empty database

engine = create_engine("sqlite:///bedfile_db.db", echo=True)

# create an empty database with the structure outlined above

Base.metadata.create_all(bind=engine)

# create session

Session = sessionmaker(bind=engine)
session = Session()

# specifying data types for DataFrame
column_types = {
    "chromosome": str,
    "start": int,
    "end": int,
    "name": str,
    "score": int,
    "strand": str
}

# reading bedfile into a DataFrame
bed_df = pd.read_csv("test_expected_4562.bed",
                     sep="\t",
                     comment="#",
                     dtype=column_types
                         )

# Insert data into database
for index, row in bed_df.iterrows():
    feature = Bedfile(
        chromosome=row["chromosome"],
        start=row["start"],
        end=row["end"],
        name=row["name"],
        score=row["score"],
        strand=row["strand"])
    session.add(feature)

session.commit()
