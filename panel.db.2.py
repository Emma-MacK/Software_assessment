import csv
import sqlalchemy
import pandas as pd

from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, Float, Boolean, insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship




Base = declarative_base()

class Panels(Base):

    __tablename__ = "panels"

    panel_id_v = Column("Panel ID and Version Number", Integer, primary_key=True)
    date = Column("Date", String)
    patient_id = Column("Patient ID", String)
    accession_no = Column("Accession Number", String)
    r_number = Column("R Number", String)
    gene_list = Column("Gene List", String)

    #relationship




    def __repr__(self):

        return f"({self.panel_id_v} {self.date} {self.patient_id} {self.accession_no} {self.r_number} {self.gene_list})"


class Genes(Base):

    __tablename__ = "genes"

    genes_table_id = Column("Genes Table ID", Integer, primary_key=True)
    panel_id_v = Column(Integer, ForeignKey("panels.Panel ID and Version Number"))
    gene_name = Column("Gene Name", String)
    hgnc_id = Column("HGNC ID", String)
    hgnc_symbol = Column("HGNC Symbol", String)
    omim_no = Column("OMIM", String)
    refseq_id = Column("Refseq ID", String)
    ensembl_select = Column("Ensembl Select", Boolean)
    main_select = Column("Main Select", Boolean)
    main_clinical = Column("Main Clinical", Boolean)

    def __repr__(self):

        return f"({self.genes_table_id} {self.panel_id_v} {self.gene_name} {self.hgnc_id} {self.hgnc_symbol} {self.omim_no} \
            {self.refseq_id} {self.ensembl_select} {self.main_select} {self.main_clinical})"



# create an empty database

engine = create_engine("sqlite:///panel_db.db", echo=True)

# create an empty database with the structure outlined above

Base.metadata.create_all(bind=engine)

# create objects and persist

with Session(engine) as session:

    session.add_all([
        Panels(panel_id_v="1", date="01012023", patient_id="1", accession_no="1", r_number="000", gene_list="gene,list"),
        Genes(genes_table_id="1", panel_id_v="1", gene_name="gene", hgnc_id="HGNC:id", hgnc_symbol="symbol", omim_no="000000", refseq_id="refseq_id", \
              ensembl_select=True, main_select=False, main_clinical=True)
    ])

    session.commit()
