import json
import pandas as pd

from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, Boolean, FLOAT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

Base = declarative_base()

'''Creation of Panels table.'''

class Panels(Base):

    __tablename__ = "panels"

    panel_table_id = Column("Panel Table ID", Integer, primary_key=True, autoincrement=True)
    panel_id_v = Column("Panel ID and Version Number", FLOAT)
    date = Column("Date", String)
    patient_id = Column("Patient ID", String)
    accession_no = Column("Accession Number", String)
    r_number = Column("R Number", String)
    gene_list = Column("Gene List", String)

    def __repr__(self):

        return f"({self.panel_id_v} {self.date} {self.patient_id} {self.accession_no} {self.r_number} {self.gene_list})"

'''Creation of Genes table.'''

class Genes(Base):

    __tablename__ = "genes"

    genes_table_id = Column("Genes Table ID", Integer, primary_key=True, autoincrement=True)
    panel_id_v = Column(String, ForeignKey("panels.Panel ID and Version Number"))
    gene_name = Column("Gene Name", String)
    hgnc_id = Column("HGNC ID", String)
    hgnc_symbol = Column("HGNC Symbol", String)
    omim_no = Column("OMIM", String)
    refseq_id = Column("Refseq ID", String)
    ensembl_select = Column("Ensembl Select", Boolean)
    mane_select = Column("Mane Select", Boolean)
    mane_plus_clinical = Column("Mane Plus Clinical", Boolean)

    def __repr__(self):

        return f"({self.genes_table_id} {self.panel_id_v} {self.gene_name} {self.hgnc_id} {self.hgnc_symbol} {self.omim_no} \
            {self.refseq_id} {self.ensembl_select} {self.mane_select} {self.mane_plus_clinical})"

class Bedfile(Base):
    """
    SQLAlchemy model representing data needed to create a
    genomic BED file.

    Attributes:
    - entry_id (int): Primary key identifier for the BED file entry.
    - gene_name (str): Gene name associated with the entry.
    - hgnc_id (int): HGNC (HUGO Gene Nomenclature Committee) identifier.
    - chromosome (str): Chromosome on which the genomic region is
    located.
    - start (int): Starting position of the genomic region.
    - end (int): Ending position of the genomic region.
    - name (str): Name or identifier associated with the entry.
    - score (int): Score associated with the entry.
    - strand (str): Strand direction of the genomic region.

    Note: gene_name and hgnc_id are foreign keys linked to the
    genes database
    """

    __tablename__ = "bedfile"

    entry_id = Column("entry_id", Integer, primary_key=True, autoincrement=True)
    gene_name = Column("Gene Name", String, ForeignKey("genes.Gene Name"))
    hgnc_id = Column("HGNC ID", String, ForeignKey("genes.HGNC ID"))
    chromosome = Column("Chromosome", String)
    start = Column("Start", Integer)
    end = Column("End", Integer)
    name = Column ("Name", String)
    score = Column ("Score", Integer)
    strand = Column ("Strand Direction", String)

# create an empty database
engine = create_engine("sqlite:///panel_db.db", echo=True)

# create an empty database with the structure outlined above
Base.metadata.create_all(bind=engine)

# create session
Session = sessionmaker(bind=engine)
session = Session()

# load json file
with open ("test_output.json", "r") as json_file:
    data = json.load(json_file)

# add data from json into Genes table
for item in data:

    new_record = Genes(**item)
    session.add(new_record)

session.commit()

# create an empty database with the structure outlined above
Base.metadata.create_all(bind=engine)

# create session
Session = sessionmaker(bind=engine)
session = Session()

# specifying data types for Pandas DataFrame
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

# Insert data into bedfile database
for index, row in bed_df.iterrows():
    feature = Bedfile(
        chromosome=row["chromosome"],
        start=row["start"],
        end=row["end"],
        name=row["name"],
        score=row["score"],
        strand=row["strand"])
    session.add(feature)

# commit
session.commit()