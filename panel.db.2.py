import csv
import sqlalchemy
import pandas as pd
import json

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
    gene_name = Column("gene_name", String)
    hgnc_id = Column("hgnc_ID", String)
    hgnc_symbol = Column("hgnc symbol", String)
    omim_no = Column("OMIM", String)
    refseq_id = Column("refseq_id", String)
    ensembl_select = Column("ensembl_select", Boolean)
    main_select = Column("main_select", Boolean)
    main_clinical = Column("main_plus_clinical", Boolean)

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
        Genes(genes_table_id="12", panel_id_v="1", gene_name="gene", hgnc_id="HGNC:id", hgnc_symbol="symbol", omim_no="000000", refseq_id="refseq_id", \
              ensembl_select=True, main_select=False, main_clinical=True)
    ])

    session.commit()




# reading json data from file

#with open("/home/stpuser/manchester/Software_assessment/123_VV_output.json") as f:
 #   json_data = json.load(f)

# converting json to pandas df

def parse(file):
    df = pd.read_json(file, orient='records', typ='series')
    return df

#path to json file
parsed_json = parse("/home/stpuser/manchester/Software_assessment/123_VV_output.json")

# adding df to database
parsed_json.to_sql(name='genes', con=engine, if_exists='replace', index=True)