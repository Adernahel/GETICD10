### crud.py ###
from Config import *
from Models import Base,Patient
from Main import PatientRandom
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
from ICD10csv import get_icd10_csv

engine = create_engine(DATABASE_URI,echo=True)
"""
def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

recreate_database()
"""
Session = sessionmaker(bind=engine)
session = Session()

def Add_New_Patients(amount):
    patient_list = []
    
    for i in range(amount):
        patient_list.append(PatientRandom())
    for obj in patient_list:
        patient = Patient(
            NaturalId = obj.NaturalId, 
            FirstName = obj.FirstName,
            LastName = obj.LastName,
            BirthDate= obj.BirthDate,  
            Gender = obj.Gender,
            Street = obj.Street,
            City = obj.City,
            ZipCode = obj.ZipCode 
        )
        session.add(patient)
        session.commit()
        session.close

def Populate_ICD10_Table(icd10_data_frame):
    df = icd10_data_frame
    df.columns = ['ICD10','Name']
    df.to_sql('diagnosisdict',con=engine, if_exists='append',index_label='id')
    engine.execute("select * from diagnosisdict").fetchall()


Populate_ICD10_Table(get_icd10_csv())
            




