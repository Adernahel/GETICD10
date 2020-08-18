import csv
import os
import pandas as pd
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
    concated_services = pd.DataFrame(columns=['ServiceName','ServiceShort'])
    for i,row in df.iterrows():
        if row['Specialty'] == 'Surgery':
            service_name_first = 'Short surgery perfomed by ' + row['Specialist titles'].lower()
            service_name_second = 'Long surgery perfomed by ' + row['Specialist titles'].lower()
            serivce_name_control = 'Control visit'

            
            service_name_short_first = "".join([word[0] for word in service_name_first.split()]).upper() 
            service_name_short_second = "".join([word[0] for word in service_name_second.split()]).upper() 
            service_name_short_control = "".join([word[0] for word in (serivce_name_control + row['Specialist titles']).split()]).capitalize() 
            
            all_services = [[service_name_first,service_name_short_first],[service_name_second,service_name_short_second],[serivce_name_control,service_name_short_control]]
            all_service_df = pd.DataFrame(all_services, columns=['ServiceName','ServiceShort'])
            concated_services = pd.concat([concated_services,all_service_df])

        elif row['Specialty'] == 'Radiology':
            service_name_first = 'One body part diagnostic performed by ' + row['Specialist titles'].lower()
            service_name_second = 'Two body parts diagnostic performed by ' + row['Specialist titles'].lower()
            service_name_third = 'Three body parts diagnostic performed by ' + row['Specialist titles'].lower()

            service_name_short_first = "".join([word[0] for word in service_name_first.split()]).upper() 
            service_name_short_second = "".join([word[0] for word in service_name_second.split()]).upper() 
            service_name_short_third = "".join([word[0] for word in service_name_third.split()]).upper() 

            all_services = [[service_name_first,service_name_short_first],[service_name_second,service_name_short_second],[service_name_third,service_name_short_third]]
            all_service_df = pd.DataFrame(all_services, columns=['ServiceName','ServiceShort'])
            concated_services = pd.concat([concated_services,all_service_df])

        else:
            service_name_first = 'Medical advice given by ' + row['Specialist titles'].lower()
            service_name_second = 'Remote medical advice given by ' + row['Specialist titles'].lower()

            service_name_short_first = "".join([word[0] for word in service_name_first.split()]).upper() 
            service_name_short_second = "".join([word[0] for word in service_name_second.split()]).upper() 

            all_services = [[service_name_first,service_name_short_first],[service_name_second,service_name_short_second]]
            all_service_df = pd.DataFrame(all_services, columns=['ServiceName','ServiceShort'])
            concated_services = pd.concat([concated_services,all_service_df])
    return concated_services

print(create_clinic_services(ccs))
        




