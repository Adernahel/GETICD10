### crud.py ###
from Config import *
from Models import Base,Patient
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


def populate_ICD10_table(icd10_data_frame):
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

def populate_patient_table(patient_data_frame):
    df = patient_data_frame
    df.to_sql('patient',con=engine, if_exists='append',index=False,index_label="id")
    engine.execute("select * from patient").fetchall()
    

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
        
def populate_schedule_tables(schedule_data_frame):
    df_schedule = schedule_data_frame

    for i,row in df_schedule.iterrows():
        role_sql = pd.read_sql(('select "id" from roles where "RoleName" = %(rname)s'),con=engine,params=({'rname':row['Specialty']}))
        employee_sql = pd.read_sql(('select "id" from employee where "LicenseNo" = %(lno)s'),con=engine,params=({'lno':str(row['Physican'])}))

        print(role_sql['id'])
        print(employee_sql['id'])
        schedule_type = 0

        schedule_dict = {'ScheduledDate':[row['dates']],'ScheduleTimeS':[row['TimeStart']],'ScheduleTimeE':[row['TimeEnd']],'ScheduleHash':str([row['Hash']])}

        df_schedule_tosql = pd.DataFrame(data=schedule_dict)

        

        df_schedule_tosql.to_sql('schedule',con=engine,if_exists='append',index=False,index_label='id')

        schedule_id = pd.read_sql(('select "id" from schedule where "ScheduleHash" = %(rhash)s'),con=engine,params=({'rhash':'[' + str(row['Hash']) + ']'}))

        print(schedule_id)

        if employee_sql.empty:
            schedule_type = 1
        else:
            schedule_type = 2

        scheduletypes_dict = {'ScheduleType':[schedule_type],'ScheduleId':[schedule_id['id'].iloc[0]],'PhysicianId':[employee_sql['id'].iloc[0]],'RoleId':[role_sql['id'].iloc[0]]}

        df_scheduletypes_tosql = pd.DataFrame(data=scheduletypes_dict)

   

        df_scheduletypes_tosql.to_sql('schedulertypes',con=engine,if_exists='append',index=False,index_label='id')





        

























