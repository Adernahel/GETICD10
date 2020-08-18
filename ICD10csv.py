import csv
import os
import pandas as pd



path_to_file = os.getcwd() + '\\' + 'ClinicDB\\ICD10en.csv'



def get_icd10_csv(csv_path):

    icd10_csv = pd.read_csv(path_to_file, sep=";",encoding="ANSI")
    
    icd10_data_frame_csv = pd.DataFrame(icd10_csv)

    icd10_data_frame_csv = icd10_data_frame_csv[["Subcategory code","subcategory"]]

    icd10_data_frame_csv = icd10_data_frame_csv[icd10_data_frame_csv["Subcategory code"] != "|"]

    return icd10_data_frame_csv.drop_duplicates()

print(get_icd10_csv(path_to_file))
