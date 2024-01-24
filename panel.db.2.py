import json

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
    panel_id_v = Column(ForeignKey("panels.Panel ID and Version Number"))
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

# add to Genes table
    
for item in data:

    new_record = Genes(**item)
    session.add(new_record)

# commit

session.commit()