import csv
import os
import pandas as pd
import numpy as ny
import random
import names
import datetime
import barnum
import re
from datetime import date
from ICD10csv import get_type2_role_csv
from ICD10csv import get_icd10_csv
from Crud import populate_employee_tables,populate_role_table,populate_employeeroles_table,populate_ICD10_table,populate_patient_table,populate_service_table, populate_schedule_tables
from pandas.util import hash_pandas_object

class PatientRandom:
    def __init__(self,Pediatric,**kwargs):
        if Pediatric == 1:
            start_date = datetime.date(2005, 1, 1)
        else:
            start_date = datetime.date(1920, 1, 1)
        end_date = datetime.date(2020, 1, 1)   
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        MaleFemale = random.randint(0, 1)
        BirthDate = start_date + datetime.timedelta(days=random_number_of_days)
        CityZip = barnum.create_city_state_zip()
        CitySlice = slice(1,2)
        ZipSlice = slice(0,1)
        x =(CityZip[CitySlice])
        y =(CityZip[ZipSlice])
        Cit = str(x).replace("\'","").replace("(","").replace(")","").replace(",","")
        ZipCod = str(y).replace("\'","").replace("(","").replace(")","").replace(",","")
        LastName = names.get_last_name()
        NaturalId = str(BirthDate).replace("-","") + str(MaleFemale) + str(random.randint(1111111,9999999))

        if MaleFemale == 0:
            FirstName = names.get_first_name(gender='male')

        if MaleFemale == 1:
            FirstName = names.get_first_name(gender='female')
        
        self.FirstName = FirstName
        self.LastName = LastName
        self.BirthDate = BirthDate
        self.Gender = MaleFemale
        self.NaturalId = NaturalId
        self.City = Cit
        self.Street = barnum.create_street()
        self.ZipCode = ZipCod

        # update properties if kwargs are passed 
        self.__dict__.update(kwargs)


def create_clinic_spec(role_data_frame):
    df = role_data_frame
    clinic_spec = df["Specialty"].sample(n=2,replace=True)
    concated_roles = pd.DataFrame(columns=['Specialty','Fields of specialty practice','Specialist titles'])
    for i in clinic_spec:

        random_role = df[df["Specialty"] == i].sample(n=2,replace=True)    
        concated_roles = pd.concat([concated_roles,random_role])
    
    return concated_roles[['Specialist titles','Specialty']]

def create_clinic_services(clinic_spec_data_frame):
    df = clinic_spec_data_frame
    concated_services = pd.DataFrame(columns=['ServiceName','ServiceShort','ServicePrice','ServiceCost','ServiceDuration'])
    for i,row in df.iterrows():
        if row['Specialty'] == 'Surgery':
            service_name_first = 'Short surgery perfomed by ' + row['Specialist titles'].lower()
            service_name_second = 'Long surgery perfomed by ' + row['Specialist titles'].lower()
            serivce_name_control = 'Surgery control visit'

            
            service_name_short_first = "".join([word[0] for word in service_name_first.split()]).upper() 
            service_name_short_second = "".join([word[0] for word in service_name_second.split()]).upper() 
            service_name_short_control = "".join([word[0] for word in serivce_name_control.split()]).capitalize() 

            base_cost = 200
            random_price_part = random.choice([100,120,140,160])

            service_price_first = (base_cost + random_price_part) * 0.75
            service_price_second = (base_cost + random_price_part) * 1.25
            service_price_control = (base_cost + random_price_part) * 0.25

            service_cost_first = random_price_part * 0.75
            service_cost_second = random_price_part * 1.25
            service_cost_control = random_price_part * 0.25

            base_duration = 20

            service_duration_first = base_duration
            service_duration_second = base_duration * 2
            service_duration_control = base_duration / 2
            
            all_services = [\
            [service_name_first,service_name_short_first,service_price_first,service_cost_first,service_duration_first]\
            ,[service_name_second,service_name_short_second,service_price_second,service_cost_second,service_duration_second]\
            ,[serivce_name_control,service_name_short_control,service_price_control,service_cost_control,service_duration_control]]

            all_service_df = pd.DataFrame(all_services, columns=['ServiceName','ServiceShort','ServicePrice','ServiceCost','ServiceDuration'])
            concated_services = pd.concat([concated_services,all_service_df])

        elif row['Specialty'] == 'Radiology':
            service_name_first = 'One body part diagnostic performed by ' + row['Specialist titles'].lower()
            service_name_second = 'Two body parts diagnostic performed by ' + row['Specialist titles'].lower()
            service_name_third = 'Three body parts diagnostic performed by ' + row['Specialist titles'].lower()

            service_name_short_first = "".join([word[0] for word in service_name_first.split()]).upper() 
            service_name_short_second = "".join([word[0] for word in service_name_second.split()]).upper() 
            service_name_short_third = "".join([word[0] for word in service_name_third.split()]).upper() 

            base_cost = 300
            random_price_part = random.choice([100,120,140,160])

            service_price_first = (base_cost + random_price_part) * 1.25
            service_price_second = (base_cost + random_price_part) * 1.50
            service_price_third = (base_cost + random_price_part) * 1.75

            service_cost_first = random_price_part * 1.25
            service_cost_second = random_price_part * 1.50
            service_cost_third = random_price_part * 1.75

            base_duration = 15

            service_duration_first = base_duration
            service_duration_second = base_duration * 1.5
            service_duration_third = base_duration * 2


            all_services = [\
            [service_name_first,service_name_short_first,service_price_first,service_cost_first,service_duration_first]\
            ,[service_name_second,service_name_short_second,service_price_second,service_cost_second,service_duration_second]\
            ,[service_name_third,service_name_short_third,service_price_third,service_cost_third,service_duration_third]]


            all_service_df = pd.DataFrame(all_services, columns=['ServiceName','ServiceShort','ServicePrice','ServiceCost','ServiceDuration'])
            concated_services = pd.concat([concated_services,all_service_df])

        else:
            service_name_first = 'Medical advice given by ' + row['Specialist titles'].lower()
            service_name_second = 'Remote medical advice given by ' + row['Specialist titles'].lower()

            service_name_short_first = "".join([word[0] for word in service_name_first.split()]).upper() 
            service_name_short_second = "".join([word[0] for word in service_name_second.split()]).upper() 

            base_cost = 100
            random_price_part = random.choice([100,120])

            service_price_first = (base_cost + random_price_part) * 1
            service_price_second = (base_cost + random_price_part) * 1.25
         

            service_cost_first = random_price_part * 1
            service_cost_second = random_price_part * 1.25
   
            base_duration = 15

            service_duration_first = base_duration
            service_duration_second = base_duration

            all_services = [\
            [service_name_first,service_name_short_first,service_price_first,service_cost_first,service_duration_first]\
            ,[service_name_second,service_name_short_second,service_price_second,service_cost_second,service_duration_second]]

            all_service_df = pd.DataFrame(all_services, columns=['ServiceName','ServiceShort','ServicePrice','ServiceCost','ServiceDuration'])
            concated_services = pd.concat([concated_services,all_service_df])
    return concated_services

def create_clinic_physician(clinic_spec_data_frame):
    df = clinic_spec_data_frame
    concated_physician = pd.DataFrame(columns=['FirstName','LastName','LicenseNo','HireDate','Age','Specialty'])


    for i,row in df.iterrows():
        FirstName = ''
        LastName = names.get_last_name()
        LicenseNo = "S" + str(row['Specialty'])[0] + str(random.randint(10000,99999))
        HireDate = date.today()
        Age = random.randint(27,80)
        Speciality = row['Specialist titles']

        MaleFemale = random.randint(0, 1)
        if MaleFemale == 0:
            FirstName = names.get_first_name(gender='male')

        if MaleFemale == 1:
            FirstName = names.get_first_name(gender='female')
        
        created_physician=[[FirstName,LastName,str(LicenseNo),HireDate,Age,Speciality]]
        created_physician_df = pd.DataFrame(created_physician,columns=['FirstName','LastName','LicenseNo','HireDate','Age','Specialty'])
        concated_physician = pd.concat([concated_physician,created_physician_df])
    
    return concated_physician

def create_clinic_first_patients(clinic_spec_data_frame):
    df = clinic_spec_data_frame
    all_patients = pd.DataFrame(columns=['FirstName','LastName','BirthDate','Gender','NaturalId','City', 'Street', 'ZipCode'])

    for i,row in df.iterrows():
        random_num_patients = random.randint(10,40)
        if row['Specialty'] == "Paediatrics and child health":
            is_child = 1
        else:
            is_child = 0
        for i in range(random_num_patients):
            random_patient_dict = PatientRandom(is_child).__dict__            
            random_patient_df = pd.DataFrame([random_patient_dict], columns=random_patient_dict.keys())
            all_patients = pd.concat([all_patients,random_patient_df])
    return all_patients 

def create_schedules(clinic_spec_data_frame,clinic_physicians,schedule_min_date,schedule_period):
    cs_df = clinic_spec_data_frame
    cp_df = clinic_physicians
    sch_min_d = datetime.datetime.strptime(schedule_min_date,'%Y-%m-%d')
    sch_max_d = sch_min_d + datetime.timedelta(days=schedule_period)
    physicans_work_week = pd.DataFrame(columns=['Physican','Day','TimeStart','TimeEnd'])

    for i,row in cp_df.iterrows():
        
        random_working_periods = random.randint(1,5)
        week_day_list = []
        physican_id = row['LicenseNo']
        physican_spec = row['Specialty']
        work_days_df = pd.DataFrame(columns=['Physican','Specialty','Day','TimeStart','TimeEnd'])

        for i in range(random_working_periods):
            random_week_day = random.randint(0,4)
            week_day_list.append(random_week_day)

        week_day_df = pd.DataFrame(week_day_list,columns=['WeekDays'])

        week_day_df = week_day_df.groupby(['WeekDays']).size().reset_index(name='counts')

        for i,row in week_day_df.iterrows():
            hour_time = 8
            row_count = row['counts']
            work_day_number = row['WeekDays']
            hour_time = (hour_time / row_count) * 3600
            min_hour = 7
            max_hour = 21 - (8 + (row_count - 1))
            min_break = 15 * 60
            max_break = 60 * 60

            start_hour = random.randrange(min_hour * 3600,max_hour * 3600, 15 * 60)

            for i in range(row_count):
                work_day = [[physican_id,physican_spec,work_day_number,start_hour,(start_hour + hour_time)]]
                work_day_df = pd.DataFrame(work_day,columns=['Physican','Specialty','Day','TimeStart','TimeEnd'])
                work_days_df = pd.concat([work_days_df,work_day_df])
                random_break_lenght = random.randrange(min_break,max_break, 5 * 60)
                start_hour = start_hour + hour_time + random_break_lenght
        
        physicans_work_week = pd.concat([physicans_work_week,work_days_df])
    
    dates_from_range_df = pd.DataFrame({'dates':pd.date_range(start=sch_min_d,end=sch_max_d)})          

    dates_from_range_df['Day'] = dates_from_range_df['dates'].dt.dayofweek
                

    work_period_df = pd.merge(dates_from_range_df,physicans_work_week,on='Day')

    work_period_df['Hash'] = hash_pandas_object(work_period_df)

    return work_period_df[['dates','Physican','Specialty','TimeStart','TimeEnd','Hash']]




type_2_roles = get_type2_role_csv()

ccs = create_clinic_spec(type_2_roles)

cp = create_clinic_physician(ccs)

cs = create_clinic_services(ccs)

cpa = create_clinic_first_patients(ccs)


csch = create_schedules(ccs,cp,'2020-09-01',30)




populate_role_table(ccs)

populate_employee_tables(cp)

populate_employeeroles_table(cp)

populate_service_table(cs)

populate_patient_table(cpa)

populate_ICD10_table(get_icd10_csv())

populate_schedule_tables(csch)
