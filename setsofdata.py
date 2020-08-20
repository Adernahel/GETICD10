import csv
import os
import pandas as pd
import random
from ICD10csv import get_type2_role_csv


type_1_roles = {'Roles': ['Physician','Receptionist'], 'RoleType' : '1' }

type_2_roles = get_type2_role_csv()

def create_clinic_spec(role_data_frame):
    df = role_data_frame
    clinic_spec = df["Specialty"].sample(n=2,replace=True)
    concated_roles = pd.DataFrame(columns=['Specialty','Fields of specialty practice','Specialist titles'])
    for i in clinic_spec:

        random_role = df[df["Specialty"] == i].sample(n=2,replace=True)    
        concated_roles = pd.concat([concated_roles,random_role])
    
    return concated_roles[['Specialist titles','Specialty']]

print(create_clinic_spec(type_2_roles))   

ccs = create_clinic_spec(type_2_roles)



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

print(create_clinic_services(ccs))
        
print('test')



