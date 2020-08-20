import requests
import json
import csv

import pandas as pd    
import numpy as np

url = 'https://api.dane.gov.pl/resources/10566,miedzynarodowa-statystyczna-klasyfikacja-chorob-i-problemow-zdrowotnych-icd10-eng-/data'


def recur(urlt):

    response = requests.get(urlt).json()
    nextlink = response['links'].get('next', None)
    
    print(nextlink)
    if nextlink:
        return(recur(nextlink))
    else:
        return None

print(recur(url))