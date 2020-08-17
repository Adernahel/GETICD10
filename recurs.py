from urllib.request import Request, urlopen
import json
import csv

import pandas as pd    
import numpy as np

url = 'https://api.dane.gov.pl/resources/10566,miedzynarodowa-statystyczna-klasyfikacja-chorob-i-problemow-zdrowotnych-icd10-eng-/data'


def recur(urlt):
    request = Request(urlt)
    response = urlopen(request)
    icd10 = response.read()
    selflink = json.loads(icd10)['links']['self']
    nextlink = json.loads(icd10)['links']['next']
    lastlink = json.loads(icd10)['links']['last']
    print(nextlink)
    if selflink != lastlink:
        return(recur(nextlink))
    else:
        return None

print(recur(url))
    




