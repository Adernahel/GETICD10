import requests
import csv
import pandas as pd
import numpy as np

url = 'https://api.dane.gov.pl/resources/10566,miedzynarodowa-statystyczna-klasyfikacja-chorob-i-problemow-zdrowotnych-icd10-eng-/data'




def getallicd10(urlpar):
    jsondata = requests.get(urlpar).json()
    icd_dataframe = pd.DataFrame(columns=['ICD10','Name','Checksum'])

    while 'next' in jsondata['links']:
        newitem = jsondata['links'].get('next')
        
        for i in requests.get(newitem).json()['data']:
            icd10p = pd.DataFrame(i)
            code = icd10p.loc['col12']['attributes']
            full_name = icd10p.loc['col13']['attributes']
            checksum = code + full_name

            temp_dict = {'ICD10': code, 'Name': full_name, 'Checksum': checksum}
            temp_dataframe = pd.DataFrame(temp_dict, index = [0])
            temp_dataframe = temp_dataframe[temp_dataframe['ICD10'] != '|']
            icd_dataframe = pd.concat([icd_dataframe,temp_dataframe])
        
        jsondata['links'] = requests.get(newitem).json()['links']
    return icd_dataframe.drop_duplicates(subset=['Checksum'])

print(getallicd10(url))