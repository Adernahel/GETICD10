import requests
import csv

import pandas as pd    
import numpy as np

def main():
    icd_dataframe = pd.DataFrame(columns=['ICD10','Name'])

    url = 'https://api.dane.gov.pl/resources/10566,miedzynarodowa-statystyczna-klasyfikacja-chorob-i-problemow-zdrowotnych-icd10-eng-/data'
    data = requests.get(url).json()['data']


    for i in data:
        icd10p = pd.DataFrame(i)
        code = icd10p.loc['col12']['attributes']
        full_name = icd10p.loc['col13']['attributes']

        temp_dict = {'ICD10': code, 'Name': full_name}
        temp_dataframe = pd.DataFrame(temp_dict, index = [0])
        icd_dataframe = pd.concat([icd_dataframe,temp_dataframe])
        

    print (icd_dataframe[icd_dataframe['ICD10'] != '|'])


if __name__ == '__main__':
    main()
    

