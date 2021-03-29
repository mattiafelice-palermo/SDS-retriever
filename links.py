#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 23:47:09 2021

@author: mattia
"""
import requests
from bs4 import BeautifulSoup
from sys import exit

CAS = '7664-41-7'
molecule_tgt = 'Ammonia'
grade_tgt = '294993'


url='https://www.sigmaaldrich.com/catalog/search?interface=CAS%20No.&term='+CAS+'&N=0&lang=it&region=IT&focus=product&mode=mode+matchall&region=global'

header = {"Accept-Encoding":"gzip, deflate, it", "Accept-Language": "it-IT,it;q=0.9", 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

soup=BeautifulSoup(open('sigma.txt'), 'html.parser')


list_tags = soup.find_all(class_="productContainer-inner")

products = {}

for product in list_tags:
    name_class = product.find(class_='name')
    name = name_class.string
    products[name] = product.find_all(class_= 'text')
    
grades = {}

for grade in products[molecule_tgt]:
    test = grade['onclick'].replace("'",'')[25:]
    code, brand  = test.split(',')[0],  test.split(',')[1]
    grades[code] = brand


SDS_url = 'https://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=IT&language=it&productNumber=294993&brand=ALDRICH&PageToGoToURL=%2Fsafety-center.html'

print(SDS_url)

s = requests.Session()

driver = s.get(SDS_url)

soup=BeautifulSoup(driver.content, 'html.parser')

test = soup.find_all('iframe', id='msdsPageFrame')

msdscontentdiv = soup.find_all('div', id="msdscontentDiv")

url = 'https://www.sigmaaldrich.com'+test[0]['src']

PDF = s.get(url)


filename = CAS + "_" + molecule_tgt + "_" + grade_tgt + ".pdf"

with open(filename, 'wb') as file:
    file.write(PDF.content)
        



