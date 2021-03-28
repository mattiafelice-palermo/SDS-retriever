#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 23:47:09 2021

@author: mattia
"""
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from sys import exit

from selenium.webdriver.firefox.options import Options
chrome_options = Options()

#chrome_options.add_argument("--disable-gpu")
chrome_options.headless = True # also works
#chrome_options.add_argument('--disable-browser-side-navigation')
#driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Firefox(options=chrome_options, executable_path=r'C:\Users\matti\anaconda3\geckodriver.exe')

CAS = '7664-41-7'
molecule_tgt = 'Ammonia'
grade_tgt = '294993'


url='https://www.sigmaaldrich.com/catalog/search?interface=CAS%20No.&term='+CAS+'&N=0&lang=it&region=IT&focus=product&mode=mode+matchall&region=global'
url='https://www.sigmaaldrich.com/catalog/search?term=7664-41-7&interface=CAS%20No.&N=0&mode=mode%20matchall&lang=en&region=global&focus=product'
#page = requests.get(url, allow_redirects=True, headers = {"Accept-Language": "it-IT;q=0.5"})
#page = urlopen(url)
header = {"Accept-Encoding":"gzip, deflate, it", "Accept-Language": "it-IT,it;q=0.9", 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
#header['Referrer'] = 'https://www.sigmaaldrich.com/catalog/search?term=MFCD00011418&interface=MDL%20No.&N=0&mode=mode%20matchall&lang=it&region=IT&focus=product'
#header['Sec-Fetch-Dest'] = 'document'
#header['Referer'] = 'https://www.sigmaaldrich.com/MSDS/MSDS/PleaseWaitMSDSPage.do?language=&country=IT&brand=ALDRICH&productNumber=294993'


#page = requests.get(url, allow_redirects=True, headers=header)



#file = open("sigma.txt", "w", encoding="utf-8")
#file.write(page.text)
#file.close()

#soup=BeautifulSoup(driver.page_source, 'html.parser')

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
    print('#########################################################')


SDS_url = 'https://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=IT&language=it&productNumber=294993&brand=ALDRICH&PageToGoToURL=%2Fsafety-center.html'

print(SDS_url)

#page = requests.get(SDS_url, headers = header)

driver.implicitly_wait(10)
driver.get(SDS_url)


soup=BeautifulSoup(driver.page_source, 'html.parser')

#test = soup.find_all(class_='msdsLinkDiv')

test = soup.find_all('iframe', id='msdsPageFrame')

url = 'https://www.sigmaaldrich.com'+test[0]['src']

PDF = requests.get(url, headers = header)

filename = CAS + "_" + molecule_tgt + "_" + grade_tgt + ".pdf"

print(url)

with open(filename, 'wb') as file:
    file.write(PDF.content)



exit()
links = []

for link in soup.find_all('a', href=True):
    links.append(link['href'])

product_links = []

for link in links:
    if link.startswith('/catalog/product/'):
        link = link.split('?')[0]
        link = 'https://www.sigmaaldrich.com' + link + '?lang=it&region=IT'
        product_links.append(link)
        
unique = set(product_links)

test = list(unique)[0]

url = test
page = requests.get(url)
soup = BeautifulSoup(page, 'html.parser')

# check here

#use CAS to change search

#then provide molecule name and grades

#molecule name is in productContainer clearfix/searchResultSubstanceBlock clearfix classmethod

#extract three search parameters from SDS javascript link

#build search query with https://www.sigmaaldrich.com/MSDS/MSDS/PleaseWaitMSDSPage.do?language=&country=IT&brand=SIAL&productNumber=402923&PageToGoToURL=https%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fsearch%3Finterface%3DCAS%2520No.%26term%3D79-11-8%26N%3D0%26lang%3Dit%26region%3DIT%26focus%3Dproduct%26mode%3Dmode%2Bmatchall

#find pdf in page

#look for c:set var="brandName" -> msdsContentDiv -> ... -> msdsLinkDiv -> iframe style ... src=''
        



