# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 17:27:13 2021

@author: matti
"""
import requests
from crawlers import get_sigmaaldrich_sds
import pandas as pd

filepath = r'C:\Users\matti\Documents\GitHub\SDS-retriever\chemicals.xlsx'
table = pd.read_excel(filepath)



sigma_table = table[table['VENDOR'] == 'Sigma-Aldrich']


headers = {"Accept-Encoding":"gzip, deflate, it", "Accept-Language": "it-IT,it;q=0.9", 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
session = requests.Session()



for row in sigma_table.itertuples():
    print('INPUT:', row[6], row[2], row[5])
    try:
        get_sigmaaldrich_sds(row[6], str(row[5]), 'IT', 'en', session)
    except ValueError as e:
        print(str(e))
    
    
