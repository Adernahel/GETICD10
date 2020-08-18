### crud.py ###
from Config import *
from Models import Base,Patient
from Main import PatientRandom
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date

engine = create_engine(DATABASE_URI,echo=True)
"""
def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

recreate_database()
"""
Session = sessionmaker(bind=engine)
session = Session()

def AddNewPatients(amount):
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




