from urllib.request import Request, urlopen
import json
import csv

import pandas as pd    
import numpy as np

url = 'https://api.dane.gov.pl/resources/10566,miedzynarodowa-statystyczna-klasyfikacja-chorob-i-problemow-zdrowotnych-icd10-eng-/data'

request = Request(url)
response = urlopen(request)
icd10 = response.read()
datal = json.loads(icd10)['data']

Icd10joined = pd.DataFrame(columns=['ICD10','Name'])


for i in datal:
    icd10p = pd.DataFrame(i)
    Code = icd10p.loc['col12']['attributes']
    FullName = icd10p.loc['col13']['attributes']
    icd10sdict = {'ICD10': Code, 'Name': FullName}
    dataframe1 = pd.DataFrame(icd10sdict, index = [0])
    Icd10joined = pd.concat([Icd10joined,dataframe1])
    

print (Icd10joined[Icd10joined['ICD10'] != '|'])



    

