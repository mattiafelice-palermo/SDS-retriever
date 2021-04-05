#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 23:47:09 2021

@author: mattia
"""
import requests
from bs4 import BeautifulSoup

def get_sigmaaldrich_sds(CAS, grade_tgt, region, language, session = None):

    url='https://www.sigmaaldrich.com/catalog/search?interface=CAS%20No.&term='+CAS+'&N=0&focus=product&mode=mode+matchall&region=global'

    headers = {"Accept-Encoding":"gzip, deflate, it", "Accept-Language": "it-IT,it;q=0.9", 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
    
    if session == None:
        session = requests.Session()

    driver = session.get(url, headers = headers)

    soup=BeautifulSoup(driver.content, 'html.parser')

    product_list = soup.find_all(class_="productContainer-inner")

    msds_list = soup.find_all(class_='msdsBulletPoint')
       
    parents = None
    brand = None
    
    for msds in msds_list:
        test = msds['href'].replace("'",'')[51:]
        code = test.split(',')[0]
        if code == grade_tgt:
           parents = msds.parents
           brand = test.split(',')[1][1:-2]
    
    if parents == None:
        #https://www.merckmillipore.com/Web-IT-Site/en_IT/-/EUR/ShowDocument-File?ProductSKU=MDA_CHEM-105012&DocumentType=MSD&DocumentId=105012_SDS_AR_ES.PDF&DocumentUID=303118&Language=ES&Country=AR&Origin=PDP
        
        raise ValueError('No SDS found')
        return

    descr = None
    name = None

    for i, parent in enumerate(parents):
        if i == 1:
            descr_tag = parent.find(class_='applicationValue')
            strings = [ string for string in descr_tag.contents[0].strings ]
            descr = ''.join(strings)
        if i == 6:
            name_tag = parent.find(class_='name')
            name = name_tag.string
            break
        
    print('OUTPUT:', grade_tgt, brand, name, descr)

    root_url = 'https://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?'

    SDS_url = root_url + 'country=' + region + '&language=' + language + '&productNumber=' + grade_tgt +'&brand=' + brand

    driver = session.get(SDS_url)

    soup=BeautifulSoup(driver.content, 'html.parser')

    js_id = soup.find_all('iframe', id='msdsPageFrame')

    url = 'https://www.sigmaaldrich.com'+js_id[0]['src']

    PDF = session.get(url)
    
    name = name.replace(' ', '-')

    filename = CAS + "_" + name + "_" + grade_tgt + '_' + region + language + ".pdf"
    

    with open(filename, 'wb') as file:
        file.write(PDF.content)
        
    return SDS_url


def get_thermofisher_SDS():
    pass

#headers = {"Accept-Encoding":"gzip, deflate, it", "Accept-Language": "it-IT,it;q=0.9", 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
#session = requests.Session()
#get_sigmaaldrich_sds('12125-02-9', '1.01145', 'IT', 'it', session)
#get_sigmaaldrich_sds('64-19-7', 'Acetic acid 30%', '1.59166', 'IT', 'it', session)

