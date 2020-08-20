### crud.py ###
from Config import *
from Models import Base,Patient
from Main import PatientRandom
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
from ICD10csv import get_icd10_csv
import pandas as pd

engine = create_engine(DATABASE_URI,echo=True)

def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

recreate_database()

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

def populate_service_table(service_data_frame):
    df = service_data_frame
    df.columns = ['ServiceName','ServiceShort','ServicePrice','ServiceCost','ServiceDuration']
    df.to_sql('services',con=engine, if_exists='append',index=False,index_label='id')
    engine.execute("select * from services").fetchall()

def populate_role_table(role_data_frame):
    df = role_data_frame
    df.columns = ['RoleName','RoleType']
    df.drop_duplicates()
    df.to_sql('roles', con=engine, if_exists='append',index=False,index_label='id')
    engine.execute("select * from roles").fetchall()


def populate_employee_tables(employee_data_frame):
    df = employee_data_frame[['FirstName','LastName','LicenseNo','HireDate','Age']]
    df.columns = ['FirstName','LastName','LicenseNo','HireDate','Age']
    df.to_sql('employee',con=engine, if_exists='append',index=False,index_label='id')
    engine.execute("select * from services").fetchall()
    
def populate_employeeroles_table(employee_data_frame):
    df_employeerole = employee_data_frame
    for i,row in df_employeerole.iterrows():
        employee_sql = pd.read_sql(('select "id" from employee where "FirstName" = %(fname)s AND "LastName" = %(lname)s AND "LicenseNo" = %(lno)s'),con=engine,\
        params=({'fname':str(row['FirstName']),'lname':str(row['LastName']),'lno':str(row['LicenseNo'])}))

        df_employee = pd.DataFrame(employee_sql,columns=(['id']))
        
        role_sql = pd.read_sql(('select "id" from roles where "RoleName" = %(rname)s'),con=engine,params=({'rname':row['Specialty']}))
        
        df_roles = pd.DataFrame(role_sql,columns=(['id']))

        df_employee['key'] = 0
        df_roles['key'] = 0
        df_employeerole_tosql = pd.merge(df_employee,df_roles, on='key')

        df_employeerole_tosql.columns = ['EmployeeId','Key','RoleId']
        df_employeerole_tosql = df_employeerole_tosql[['EmployeeId','RoleId']]

        df_employeerole_tosql.to_sql('employeeroles',con=engine, if_exists='append',index=False,index_label='id')
        
        














