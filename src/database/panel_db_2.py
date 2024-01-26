"""
genomic_database.py

This module defines SQLAlchemy models representing genomic data
for panels/case runs, genes per panel, and bedfile data.
It also creates an SQLite database with the specified structure.

Module Classes:
- Panels: Represents panel data for each patient
- Genes: Represents gene data for each available panel
- Bedfile: Represents data needed to create a genomic BED file

Database Structure:
- Foreign key relationships between Panels and Genes based on
'panel_id_v'.
- Further foreign key relationships between Genes and Bedfile
based on 'hgnc_id' and 'refseq_id'.
"""

from sqlalchemy import (create_engine, ForeignKey,
                        Column, String, Integer, Boolean)
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


# creating database structure
class Panels(Base):
    """
    SQLAlchemy model representing panel data that was run for each
    patient

    Attributes:
    - panel_table_id (int): Primary key identifier for the case entry
    - panel_id_v (Str): The RCode_panelID_panelversion of the panel run
    - date (Str): The date the case was analysed
    - patient_id (Str): The unique patient ID assigned to in-house
    - accession_no (Str): The unique ID associated with this test
    request
    - r_number (Str): The genomic test directory Rnumber assoicated with
    this test request
    - gene_list (Str): The List of Genes included in the panel

    Note: There is foreign key relationship for panel_id_v between this
    database and the genes database
    """

    __tablename__ = "panels"

    panel_table_id = Column("Panel Table ID", Integer,
                            primary_key=True, autoincrement=True)
    panel_id_v = Column("Panel ID and Version",
                        String, ForeignKey("genes.Panel ID and Version"))
    date = Column("Date", String)
    patient_id = Column("Patient ID", String)
    accession_no = Column("Accession Number", String)
    r_number = Column("R Number", String)
    gene_list = Column("Gene List", String)

    def __repr__(self):

        return f"({self.panel_id_v} {self.date} \
                  {self.patient_id} {self.accession_no} \
                  {self.r_number} {self.gene_list})"


class Genes(Base):
    """
    SQLAlchemy model representing gene data for each available panel

    Attributes:
    - genes_table_id (int): Primary key identifier for the genes table
    - panel_id_v (Str): The RCode_panelID_panelversion of the panel run
    - gene_name (Str): Gene Name
    - hgnc_id (Str): HUGO Gene Nomenclature Committee ID for the gene
    - hgnc_symbol(Str): HGNC approved Gene Symbol
    - omim_no (Str):
    - refseq_id (Str): Transcript ID
    - ensembl_select (bool): True/False wether transcript is ensembl
    select
    - mane_select (bool): True/False wether transcript is mane
    select
    - mane_plus_clinical (bool): True/False wether transcript is
    mane plus clinical

    Note: There is foreign key relationship for panel_id_v between
    this database and the panels database.
    There is also a further foreign key relationship for hgnc_id
    and refseq id between this database and the bedfile database.
    """

    __tablename__ = "genes"

    genes_table_id = Column("Genes Table ID", Integer,
                            primary_key=True, autoincrement=True)
    panel_id_v = Column("Panel ID and Version", String,
                        ForeignKey("panels.Panel ID and Version"))
    gene_name = Column("Gene Name", String)
    hgnc_id = Column("HGNC ID", String, ForeignKey("bedfile.HGNC ID"))
    hgnc_symbol = Column("HGNC Symbol", String)
    omim_no = Column("OMIM", String)
    refseq_id = Column("Refseq ID", String, ForeignKey("bedfile.Refseq ID"))
    ensembl_select = Column("Ensembl Select", Boolean)
    mane_select = Column("Mane Select", Boolean)
    mane_plus_clinical = Column("Mane Plus Clinical", Boolean)

    def __repr__(self):

        return f"({self.genes_table_id} {self.panel_id_v} {self.gene_name} \
            {self.hgnc_id} {self.hgnc_symbol} {self.omim_no} {self.refseq_id} \
            {self.ensembl_select} {self.mane_select} \
            {self.mane_plus_clinical})"


class Bedfile(Base):
    """
    SQLAlchemy model representing data needed to create a
    genomic BED file.

    Attributes:
    - entry_id (int): Primary key identifier for the BED file entry.
    - hgnc_id (int): HGNC (HUGO Gene Nomenclature Committee) identifier.
    - chromosome (str): Chromosome on which the genomic region is
    located.
    - start (int): Starting position of the genomic region.
    - end (int): Ending position of the genomic region.
    - name (str): Name or identifier associated with the entry.
    - score (int): Score associated with the entry.
    - strand (str): Strand direction of the genomic region.

    Note: There is also a further foreign key relationship for hgnc_id
    and refseq between this database and the genes database.
    """

    __tablename__ = "bedfile"

    entry_id = Column("entry_id", Integer,
                      primary_key=True, autoincrement=True)
    hgnc_id = Column("HGNC ID", String, ForeignKey("genes.HGNC ID"))
    refseq_id = Column("Refseq ID", String, ForeignKey("genes.Refseq ID"))
    chromosome = Column("Chromosome", String)
    start = Column("Start", Integer)
    end = Column("End", Integer)
    name = Column("Name", String)
    score = Column("Score", Integer)
    strand = Column("Strand Direction", String)


# create an empty database
engine = create_engine("sqlite:///panel_db.db", echo=True)

# create an empty database with the structure outlined above
Base.metadata.create_all(bind=engine)
